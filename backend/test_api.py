"""
=============================================================================
Smart Mess API Test Suite
=============================================================================
Runs comprehensive automated verification against FastAPI endpoints
using TestClient.
=============================================================================
"""

import sys
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_api_workflow():
    print("--- 1. Testing Health Check ---")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[PASS] Health check OK:", res.json())

    print("\n--- 2. Testing Menus ---")
    res = client.get("/api/menus")
    assert res.status_code == 200
    menus = res.json()
    assert len(menus) == 3
    print(f"[PASS] Retrieved {len(menus)} meal menus: {[m['meal_type'] for m in menus]}")

    print("\n--- 3. Testing Student Profile ---")
    res = client.get("/api/student/std_supriya")
    assert res.status_code == 200
    profile = res.json()
    assert profile["name"] == "Supriya"
    print(f"[PASS] Retrieved student profile: {profile['name']} ({profile['roll_number']})")

    print("\n--- 4. Testing Meal Booking & Duplicate Prevention ---")
    test_date = "2026-10-15"
    payload = {
        "student_id": "std_supriya",
        "student_name": "Supriya",
        "meal_type": "Lunch",
        "date": test_date
    }
    # First booking must succeed
    res = client.post("/api/bookings", json=payload)
    assert res.status_code in [201, 400]
    if res.status_code == 201:
        print("[PASS] Booking created successfully:", res.json()["booking"]["id"])
    else:
        print("[PASS] Already booked previously.")

    # Duplicate booking attempt must be strictly rejected
    res_dup = client.post("/api/bookings", json=payload)
    assert res_dup.status_code == 400, "Duplicate booking was NOT rejected!"
    print("[PASS] Duplicate booking successfully blocked with HTTP 400:", res_dup.json()["detail"])

    print("\n--- 5. Testing Student Bookings Query ---")
    res = client.get("/api/student/std_supriya/bookings")
    assert res.status_code == 200
    bookings = res.json()
    assert any(b["date"] == test_date and b["meal_type"] == "Lunch" for b in bookings)
    print(f"[PASS] Verified booking present in student bookings list: {len(bookings)} bookings total")

    print("\n--- 6. Testing Cancellation Flow ---")
    res_cancel = client.post("/api/bookings/cancel", json={
        "student_id": "std_supriya",
        "meal_type": "Lunch",
        "date": test_date
    })
    assert res_cancel.status_code == 200
    print("[PASS] Booking cancelled successfully:", res_cancel.json()["message"])

    # Verify cancelled booking is no longer active
    res = client.get("/api/student/std_supriya/bookings")
    assert not any(b["date"] == test_date and b["meal_type"] == "Lunch" for b in res.json())
    print("[PASS] Confirmed booking removed from active list")

    print("\n--- 7. Testing AI Demand Prediction ---")
    pred_res = client.post("/api/predict", json={
        "meal_type": "Lunch",
        "date": "2026-10-16",
        "safety_buffer": 0.08,
        "booking_count": 420
    })
    assert pred_res.status_code == 200
    pdata = pred_res.json()
    assert "predicted_attendance" in pdata
    assert "recommended_preparation" in pdata
    print(f"[PASS] AI Prediction: Booked: {pdata['booking_count']} -> Predicted Demand: {pdata['predicted_attendance']} -> Recommended Prep: {pdata['recommended_preparation']} (Buffer: +{pdata['safety_buffer_portions']})")

    print("\n--- 8. Testing Admin Summary ---")
    admin_res = client.get("/api/admin/summary?date=2026-10-16")
    assert admin_res.status_code == 200
    summary = admin_res.json()
    assert "meals" in summary
    print(f"[PASS] Admin Summary for {summary['date']}: Total Bookings: {summary['total_bookings']}")

    print("\n--- 9. Testing Preparation Logging ---")
    prep_res = client.post("/api/admin/preparation", json={
        "date": "2026-10-16",
        "meal_type": "Lunch",
        "actual_prepared": 410,
        "actual_served": 385,
        "safety_buffer_pct": 0.08,
        "notes": "Test service log"
    })
    assert prep_res.status_code == 200
    prep_data = prep_res.json()["data"]
    assert prep_data["leftover_portions"] == 25
    assert prep_data["waste_percentage"] == 6.1
    print(f"[PASS] Prep Log recorded: Prepared: {prep_data['actual_prepared']}, Served: {prep_data['actual_served']}, Leftover: {prep_data['leftover_portions']}, Waste: {prep_data['waste_percentage']}%")

    print("\n--- 10. Testing Dish-wise Waste Tracking ---")
    dish_waste_res = client.post("/api/admin/waste/dishes", json={
        "date": "2026-10-16",
        "meal_type": "Lunch",
        "dishes": [
            {"dish_name": "Steamed Rice", "prepared_portions": 200, "served_portions": 190, "reason_category": "Standard surplus"},
            {"dish_name": "Sambar", "prepared_portions": 150, "served_portions": 135, "reason_category": "Over-preparation"}
        ]
    })
    assert dish_waste_res.status_code == 200
    assert len(dish_waste_res.json()["records"]) == 2
    print("[PASS] Recorded dish-wise waste successfully")

    print("\n--- 11. Testing Waste Analytics Dashboard Data ---")
    analytics_res = client.get("/api/analytics/waste")
    assert analytics_res.status_code == 200
    analytics = analytics_res.json()
    assert "waste_by_meal" in analytics
    assert "waste_by_dish" in analytics
    assert "daily_trends" in analytics
    assert "actionable_recommendations" in analytics
    print(f"[PASS] Waste Analytics fetched: Overall Waste: {analytics['summary']['overall_waste_percentage']}%, Recs: {len(analytics['actionable_recommendations'])}")

    print("\n--- 12. Testing ML Model Metrics ---")
    metrics_res = client.get("/api/ml/metrics")
    assert metrics_res.status_code == 200
    metrics = metrics_res.json()
    assert "test_mae" in metrics
    print(f"[PASS] Model Metrics verified: MAE: {metrics['test_mae']}, R2: {metrics['test_r2']}, Algorithm: {metrics['algorithm']}")

    print("\n==============================================")
    print("ALL 12 BACKEND & ML TESTS PASSED CLEANLY!")
    print("==============================================")

if __name__ == "__main__":
    test_api_workflow()
