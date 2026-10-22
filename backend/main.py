"""
=============================================================================
FastAPI Main Application for Smart Mess Meal System
=============================================================================
Provides REST endpoints for:
- Student Pre-booking & Cancellation
- Menu Information & Timings
- AI Machine Learning Demand Predictions & Configurable Safety Buffers
- Kitchen Food Preparation & Serving Logs
- Dish-Wise Food Waste Tracking & Real-Time Analytics
=============================================================================
"""

import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    BookingRequest,
    CancelBookingRequest,
    PrepLogEntry,
    MealWasteSubmission,
    PredictionRequest
)
from .data.mess_menu import (
    get_menu_for_date,
    get_all_monthly_menus
)
from .database import (
    init_db,
    get_student_profile,
    get_all_menus,
    get_student_bookings,
    create_booking,
    cancel_booking,
    get_booking_count_for_meal,
    get_admin_dashboard_summary,
    record_meal_preparation_and_serving,
    record_dish_waste_list,
    get_waste_analytics,
    IS_SUPABASE_CONFIGURED
)
from .ml.predictor import DemandPredictor

app = FastAPI(
    title="AI-Powered Smart Mess System API",
    description="Backend API for meal pre-booking, demand prediction, and food waste reduction.",
    version="1.0.0"
)

# Enable CORS for Vite frontend (typically localhost:5173 or other local ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = DemandPredictor()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Smart Mess AI Backend",
        "database_mode": "Supabase Cloud" if IS_SUPABASE_CONFIGURED else "Zero-Config Local SQLite (Persistent & Demo Ready)",
        "timestamp": datetime.datetime.now().isoformat()
    }

# =========================================================================
# Student & Menu Endpoints
# =========================================================================

@app.get("/api/menus")
def get_menus(date: Optional[str] = Query(None)):
    """Returns active meal menus with timings and dish lists for a specific date or today."""
    return get_menu_for_date(date)

@app.get("/api/menus/month")
def get_monthly_menus():
    """Returns complete 31-day hostel mess timetable."""
    return get_all_monthly_menus()

@app.get("/api/student/{student_id}")
def get_student(student_id: str):
    profile = get_student_profile(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return profile

@app.get("/api/student/{student_id}/bookings")
def get_bookings(student_id: str):
    """Retrieves all confirmed bookings for a specific student."""
    return get_student_bookings(student_id)

@app.post("/api/bookings", status_code=status.HTTP_201_CREATED)
def book_meal(request: BookingRequest):
    """
    Books a meal for a student on a specific date.
    Strictly prevents duplicate bookings for the same student, date, and meal.
    """
    try:
        booking = create_booking(
            student_id=request.student_id,
            student_name=request.student_name,
            meal_type=request.meal_type,
            date=request.date
        )
        return {
            "success": True,
            "message": f"Successfully booked {request.meal_type} for {request.date}",
            "booking": booking
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Booking error: {str(e)}")

@app.post("/api/bookings/cancel")
def cancel_student_booking(request: CancelBookingRequest):
    """Cancels a previously booked meal."""
    success = cancel_booking(
        student_id=request.student_id,
        meal_type=request.meal_type,
        date=request.date
    )
    if not success:
        raise HTTPException(status_code=404, detail="Active booking not found to cancel")
    return {
        "success": True,
        "message": f"Booking for {request.meal_type} on {request.date} successfully cancelled"
    }

# =========================================================================
# AI Demand Prediction Endpoints
# =========================================================================

@app.post("/api/predict")
def predict_meal_demand(req: PredictionRequest):
    """
    Executes ML inference using scikit-learn regressor.
    Predicts turnout demand and computes recommended preparation quantity with safety buffer.
    """
    # If booking count is not explicitly provided in the request body, read from database
    booking_cnt = req.booking_count
    if booking_cnt is None:
        booking_cnt = get_booking_count_for_meal(req.date, req.meal_type)

    prediction_result = predictor.predict_demand(
        meal_type=req.meal_type,
        booking_count=booking_cnt,
        date_str=req.date,
        safety_buffer=req.safety_buffer
    )

    return prediction_result

@app.get("/api/ml/metrics")
def get_ml_metrics():
    """Returns explainable model evaluation statistics and feature weights."""
    return predictor.metadata

# =========================================================================
# Administrator & Food Waste Endpoints
# =========================================================================

@app.get("/api/admin/summary")
def get_admin_summary(date: Optional[str] = None):
    """Returns booking counts, meal schedule, and preparation status for the admin dashboard."""
    target_date = date or datetime.date.today().isoformat()
    summary = get_admin_dashboard_summary(target_date)

    # Attach AI predictions for each meal
    for meal_type, data in summary["meals"].items():
        pred = predictor.predict_demand(
            meal_type=meal_type,
            booking_count=data["booking_count"],
            date_str=target_date,
            safety_buffer=0.08
        )
        data["ai_prediction"] = pred

    return summary

@app.post("/api/admin/preparation")
def log_meal_preparation(entry: PrepLogEntry):
    """Logs portions prepared and portions served, computing leftover count and waste percentage."""
    try:
        result = record_meal_preparation_and_serving(entry.model_dump())
        return {
            "success": True,
            "message": f"Preparation and serving recorded for {entry.meal_type}",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/admin/waste/dishes")
def log_dish_waste(submission: MealWasteSubmission):
    """Records individual dish leftover portions and waste percentages."""
    try:
        dish_dicts = [d.model_dump() for d in submission.dishes]
        results = record_dish_waste_list(
            date_str=submission.date,
            meal_type=submission.meal_type,
            dishes=dish_dicts,
            notes=submission.notes or ""
        )
        return {
            "success": True,
            "message": f"Recorded waste for {len(results)} dishes in {submission.meal_type}",
            "records": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/waste")
def get_waste_dashboard_analytics():
    """Consolidated waste analytics: dish waste, meal waste, daily trends, and AI recommendations."""
    return get_waste_analytics()
