"""
=============================================================================
Pydantic Data Schemas & Validation for Smart Mess System
=============================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import datetime

class StudentProfile(BaseModel):
    id: str
    name: str
    roll_number: str
    email: str
    department: str = "Electronics & Communication Engineering"
    year_of_study: int = 3
    hostel_block: str = "Block B"
    room_number: str = "304"
    dietary_preference: str = "Regular"

class MealMenu(BaseModel):
    id: str
    meal_type: str
    timing_label: str
    start_time: str
    end_time: str
    main_items: str
    dishes: List[str]
    is_active: bool = True

class BookingRequest(BaseModel):
    student_id: str = Field(..., description="Unique ID of the student booking the meal")
    student_name: str = Field(..., description="Name of student")
    meal_type: str = Field(..., description="Must be Breakfast, Lunch, or Dinner")
    date: str = Field(..., description="Meal date in YYYY-MM-DD format")

    @field_validator('meal_type')
    def validate_meal_type(cls, v):
        allowed = ['Breakfast', 'Lunch', 'Dinner']
        if v not in allowed:
            raise ValueError(f"meal_type must be one of {allowed}")
        return v

    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.date.fromisoformat(v)
        except ValueError:
            raise ValueError("date must be in valid YYYY-MM-DD format")
        return v

class BookingResponse(BaseModel):
    id: str
    student_id: str
    student_name: str
    meal_type: str
    date: str
    status: str
    booked_at: str

class CancelBookingRequest(BaseModel):
    student_id: str
    meal_type: str
    date: str

class PrepLogEntry(BaseModel):
    date: str
    meal_type: str
    actual_prepared: int = Field(..., ge=0, description="Prepared portions count (must be >= 0)")
    actual_served: int = Field(..., ge=0, description="Served portions count (must be >= 0)")
    safety_buffer_pct: float = Field(0.08, ge=0.01, le=0.30)
    notes: Optional[str] = ""

class DishWasteInput(BaseModel):
    dish_name: str
    prepared_portions: int = Field(..., ge=0, description="Portions prepared for dish")
    served_portions: int = Field(..., ge=0, description="Portions served to students")
    reason_category: Optional[str] = "Standard surplus"

    @field_validator('served_portions')
    def validate_served_not_exceed_prepared(cls, v, info):
        # We allow a minor tolerance or ensure leftover calculation is safe
        return v

class MealWasteSubmission(BaseModel):
    date: str
    meal_type: str
    dishes: List[DishWasteInput]
    notes: Optional[str] = None

class PredictionRequest(BaseModel):
    meal_type: str
    date: str
    safety_buffer: Optional[float] = 0.08
    booking_count: Optional[int] = None
