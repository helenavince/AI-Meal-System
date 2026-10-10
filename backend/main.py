from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import connection
from pydantic import BaseModel

import os
import math
import joblib
import pandas as pd


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI()


# =========================================================
# LOAD AI MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "meal_demand_model.pkl"
)

model = joblib.load(MODEL_PATH)

print("ML model loaded successfully!")


# =========================================================
# CORS CONFIGURATION
# =========================================================


# CORS CONFIGURATION
frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_URLS",
        "http://localhost:5173,http://localhost:5174"
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Smart Mess API is running!"
    }


# =========================================================
# GET ALL CURRENT / UPCOMING MEALS
# =========================================================
@app.get("/meals")

def get_meals():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            meal_id,
            meal_name,
            meal_type,
            meal_date,
            meal_time
        FROM meals
        WHERE meal_date >= CURRENT_DATE
        ORDER BY meal_date, meal_time;
    """)

    rows = cursor.fetchall()

    cursor.close()

    meals = []

    for row in rows:

        meals.append({

            "meal_id": row[0],
            "meal_name": row[1],
            "meal_type": row[2],
            "meal_date": str(row[3]),
            "meal_time": str(row[4])

        })

    return meals


# =========================================================
# BOOKING REQUEST MODEL
# =========================================================

class BookingRequest(BaseModel):

    student_id: int
    meal_id: int


# =========================================================
# CREATE BOOKING
# =========================================================

@app.post("/bookings")
def create_booking(booking: BookingRequest):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT booking_id
        FROM bookings
        WHERE student_id = %s
        AND meal_id = %s
        AND status = 'BOOKED';
    """, (
        booking.student_id,
        booking.meal_id
    ))

    existing_booking = cursor.fetchone()

    if existing_booking is not None:

        cursor.close()

        return {
            "success": False,
            "message": "You have already booked this meal."
        }

    cursor.execute("""
        INSERT INTO bookings
        (
            student_id,
            meal_id
        )
        VALUES
        (
            %s,
            %s
        )
        RETURNING booking_id;
    """, (
        booking.student_id,
        booking.meal_id
    ))

    booking_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

    return {

        "success": True,

        "message": "Meal booked successfully!",

        "booking_id": booking_id,

        "student_id": booking.student_id,

        "meal_id": booking.meal_id

    }


# =========================================================
# LOGIN REQUEST MODEL
# =========================================================

class LoginRequest(BaseModel):

    email: str
    password: str


# =========================================================
# STUDENT LOGIN
# =========================================================

@app.post("/login")
def login(student: LoginRequest):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            student_id,
            name,
            email
        FROM students
        WHERE email = %s
        AND password = %s;
    """, (
        student.email,
        student.password
    ))

    row = cursor.fetchone()

    cursor.close()

    if row is None:

        return {

            "success": False,

            "message": "Invalid email or password"

        }

    return {

        "success": True,

        "student_id": row[0],

        "name": row[1],

        "email": row[2]

    }


# =========================================================
# GET STUDENT BOOKINGS
# =========================================================

@app.get("/bookings/{student_id}")
def get_student_bookings(student_id: int):

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            b.booking_id,
            s.name,
            m.meal_name,
            m.meal_type,
            m.meal_date,
            m.meal_time,
            b.status
        FROM bookings b
        JOIN students s
            ON b.student_id = s.student_id
        JOIN meals m
            ON b.meal_id = m.meal_id
        WHERE b.student_id = %s
        ORDER BY b.booking_date DESC;
    """, (student_id,))

    rows = cursor.fetchall()

    cursor.close()

    bookings = []

    for row in rows:

        bookings.append({

            "booking_id": row[0],

            "student_name": row[1],

            "meal_name": row[2],

            "meal_type": row[3],

            "meal_date": str(row[4]),

            "meal_time": str(row[5]),

            "status": row[6]

        })

    return bookings


# =========================================================
# CANCEL BOOKING
# =========================================================

@app.put("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: int):

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE bookings
        SET status = 'CANCELLED'
        WHERE booking_id = %s
        RETURNING booking_id;
    """, (booking_id,))

    row = cursor.fetchone()

    connection.commit()

    cursor.close()

    if row is None:

        return {

            "success": False,

            "message": "Booking not found"

        }

    return {

        "success": True,

        "message": "Booking cancelled successfully!",

        "booking_id": row[0]

    }


# =========================================================
# ADMIN - TOTAL BOOKING COUNT
# =========================================================

@app.get("/admin/booking-count")
def get_booking_count():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM bookings
        WHERE status = 'BOOKED';
    """)

    count = cursor.fetchone()[0]

    cursor.close()

    return {

        "total_bookings": count

    }


# =========================================================
# ADMIN - MEAL COUNTS
# =========================================================

@app.get("/admin/meal-counts")
def get_meal_counts():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            m.meal_type,
            COUNT(b.booking_id)
        FROM meals m
        LEFT JOIN bookings b
            ON m.meal_id = b.meal_id
            AND b.status = 'BOOKED'
        GROUP BY m.meal_type
        ORDER BY m.meal_type;
    """)

    rows = cursor.fetchall()

    cursor.close()

    counts = []

    for row in rows:

        counts.append({

            "meal_type": row[0],

            "booking_count": row[1]

        })

    return counts


# =========================================================
# ADMIN - TODAY'S MEALS
# =========================================================

@app.get("/admin/today-meals")
def get_today_meals():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            m.meal_id,
            m.meal_name,
            m.meal_type,
            m.meal_date,
            m.meal_time,

            COUNT(
                CASE
                    WHEN b.status = 'BOOKED'
                    THEN b.booking_id
                END
            )::INT AS active_bookings,

            COUNT(
                CASE
                    WHEN b.status = 'COMPLETED'
                    THEN b.booking_id
                END
            )::INT AS completed_bookings

        FROM meals m

        LEFT JOIN bookings b
            ON m.meal_id = b.meal_id

        WHERE m.meal_date = CURRENT_DATE

        GROUP BY
            m.meal_id,
            m.meal_name,
            m.meal_type,
            m.meal_date,
            m.meal_time

        ORDER BY m.meal_time;
    """)

    rows = cursor.fetchall()

    cursor.close()

    meals = []

    for row in rows:

        meals.append({

            "meal_id": row[0],

            "meal_name": row[1],

            "meal_type": row[2],

            "meal_date": str(row[3]),

            "meal_time": str(row[4]),

            "active_bookings": row[5],

            "completed_bookings": row[6]

        })

    return meals


# =========================================================
# MEAL REQUEST MODEL
# =========================================================

class MealRequest(BaseModel):

    meal_name: str
    meal_type: str
    meal_date: str
    meal_time: str


# =========================================================
# ADMIN - ADD MEAL
# =========================================================

@app.post("/admin/meals")
def add_meal(meal: MealRequest):

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO meals
        (
            meal_name,
            meal_type,
            meal_date,
            meal_time
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        RETURNING meal_id;
    """, (
        meal.meal_name,
        meal.meal_type,
        meal.meal_date,
        meal.meal_time
    ))

    meal_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

    return {

        "success": True,

        "message": "Meal added successfully!",

        "meal_id": meal_id

    }


# =========================================================
# FOOD WASTE REQUEST MODEL
# =========================================================

class WasteRequest(BaseModel):

    meal_id: int
    prepared_quantity: int
    consumed_quantity: int


# =========================================================
# ADMIN - RECORD FOOD WASTE
# =========================================================

@app.post("/admin/food-waste")
def add_food_waste(waste: WasteRequest):

    if waste.prepared_quantity < 0:

        return {

            "success": False,

            "message":
                "Prepared quantity cannot be negative."

        }

    if waste.consumed_quantity < 0:

        return {

            "success": False,

            "message":
                "Consumed quantity cannot be negative."

        }

    if waste.consumed_quantity > waste.prepared_quantity:

        return {

            "success": False,

            "message":
                "Consumed quantity cannot be greater than prepared quantity."

        }

    waste_quantity = (
        waste.prepared_quantity
        -
        waste.consumed_quantity
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO food_waste
        (
            meal_id,
            prepared_quantity,
            consumed_quantity,
            waste_quantity
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        RETURNING waste_id;
    """, (
        waste.meal_id,
        waste.prepared_quantity,
        waste.consumed_quantity,
        waste_quantity
    ))

    waste_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()

    return {

        "success": True,

        "message":
            "Food waste recorded successfully!",

        "waste_id":
            waste_id,

        "waste_quantity":
            waste_quantity

    }


# =========================================================
# ADMIN - COMPLETE MEAL
# =========================================================

@app.put("/admin/meals/{meal_id}/complete")
def complete_meal(meal_id: int):

    cursor = connection.cursor()


    # =====================================================
    # CHECK WHETHER MEAL EXISTS
    # =====================================================

    cursor.execute("""
        SELECT meal_id
        FROM meals
        WHERE meal_id = %s;
    """, (meal_id,))

    meal = cursor.fetchone()

    if meal is None:

        cursor.close()

        return {

            "success": False,

            "message": "Meal not found"

        }


    # =====================================================
    # MARK ACTIVE BOOKINGS AS COMPLETED
    # =====================================================

    cursor.execute("""
        UPDATE bookings
        SET status = 'COMPLETED'
        WHERE meal_id = %s
        AND status = 'BOOKED';
    """, (meal_id,))

    completed_count = cursor.rowcount


    # =====================================================
    # SAVE CHANGES
    # =====================================================

    connection.commit()

    cursor.close()


    return {

        "success": True,

        "meal_id": meal_id,

        "completed_bookings": completed_count,

        "message": "Meal completed successfully"

    }


# =========================================================
# ADMIN - FOOD WASTE SUMMARY
# =========================================================

@app.get("/admin/food-waste-summary")
def get_food_waste_summary():

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(prepared_quantity), 0),
            COALESCE(SUM(consumed_quantity), 0),
            COALESCE(SUM(waste_quantity), 0)
        FROM food_waste;
    """)

    row = cursor.fetchone()

    cursor.close()

    total_prepared = row[0]

    total_consumed = row[1]

    total_waste = row[2]

    if total_prepared > 0:

        waste_percentage = (
            total_waste
            /
            total_prepared
        ) * 100

    else:

        waste_percentage = 0

    return {

        "total_prepared":
            total_prepared,

        "total_consumed":
            total_consumed,

        "total_waste":
            total_waste,

        "waste_percentage":
            round(
                waste_percentage,
                2
            )

    }


# =========================================================
# AI MEAL DEMAND PREDICTION
# =========================================================

@app.get("/admin/meal-prediction")
def meal_prediction():

    cursor = connection.cursor()


    # =====================================================
    # 1. TOTAL STUDENTS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM students;
    """)

    total_students = cursor.fetchone()[0]


    # =====================================================
    # 2. CURRENT / UPCOMING MEALS
    # =====================================================

    cursor.execute("""
        WITH booking_data AS (

            SELECT
                meal_id,
                COUNT(*) AS booking_count
            FROM bookings
            WHERE status = 'BOOKED'
            GROUP BY meal_id

        ),

        waste_data AS (

            SELECT
                meal_id,
                SUM(prepared_quantity) AS prepared_quantity,
                SUM(waste_quantity) AS waste_quantity
            FROM food_waste
            GROUP BY meal_id

        )

        SELECT
            m.meal_id,
            m.meal_name,
            m.meal_type,
            m.meal_date,

            COALESCE(
                b.booking_count,
                0
            ) AS booking_count,

            COALESCE(
                w.prepared_quantity,
                0
            ) AS prepared_quantity,

            COALESCE(
                w.waste_quantity,
                0
            ) AS waste_quantity

        FROM meals m

        LEFT JOIN booking_data b
            ON m.meal_id = b.meal_id

        LEFT JOIN waste_data w
            ON m.meal_id = w.meal_id

        WHERE m.meal_date >= CURRENT_DATE

        ORDER BY
            m.meal_date,
            m.meal_time;
    """)

    current_meals = cursor.fetchall()


    # =====================================================
    # 3. HISTORICAL AVERAGE BOOKINGS
    # =====================================================

    cursor.execute("""
        SELECT
            m.meal_type,

            COUNT(b.booking_id)::FLOAT
            /
            COUNT(DISTINCT m.meal_id)
            AS average_bookings

        FROM meals m

        JOIN bookings b
            ON m.meal_id = b.meal_id

        WHERE b.status = 'COMPLETED'

        GROUP BY m.meal_type;
    """)

    historical_rows = cursor.fetchall()


    # =====================================================
    # 4. HISTORICAL FOOD WASTE
    # =====================================================

    cursor.execute("""
        SELECT
            m.meal_type,

            COALESCE(
                SUM(fw.prepared_quantity),
                0
            ) AS prepared_quantity,

            COALESCE(
                SUM(fw.waste_quantity),
                0
            ) AS waste_quantity

        FROM meals m

        JOIN food_waste fw
            ON m.meal_id = fw.meal_id

        WHERE m.meal_date < CURRENT_DATE

        GROUP BY m.meal_type;
    """)

    waste_rows = cursor.fetchall()

    cursor.close()


    # =====================================================
    # 5. STORE HISTORICAL DEMAND
    # =====================================================

    historical_demand = {}

    for row in historical_rows:

        meal_type = row[0]

        average_bookings = row[1]

        historical_demand[meal_type] = average_bookings


    # =====================================================
    # 6. STORE HISTORICAL WASTE
    # =====================================================

    historical_waste = {}

    for row in waste_rows:

        meal_type = row[0]

        prepared = row[1]

        waste = row[2]

        if prepared > 0:

            waste_percentage = (
                waste
                /
                prepared
            ) * 100

        else:

            waste_percentage = 0

        historical_waste[meal_type] = waste_percentage


    # =====================================================
    # 7. MEAL TYPE MAPPING
    # =====================================================

    meal_mapping = {

        "Breakfast": 0,

        "Lunch": 1,

        "Snacks": 2,

        "Dinner": 3

    }


    predictions = []


    # =====================================================
    # 8. PROCESS EACH CURRENT MEAL
    # =====================================================

    for row in current_meals:

        meal_id = row[0]

        meal_name = row[1]

        meal_type = row[2]

        meal_date = row[3]

        current_bookings = row[4]

        prepared_quantity = row[5]

        waste_quantity = row[6]


        # =================================================
        # CURRENT WASTE PERCENTAGE
        # =================================================

        if prepared_quantity > 0:

            current_waste_percentage = (
                waste_quantity
                /
                prepared_quantity
            ) * 100

        else:

            current_waste_percentage = 0


        # =================================================
        # USE HISTORICAL WASTE IF CURRENT DATA
        # IS NOT AVAILABLE
        # =================================================

        if prepared_quantity == 0:

            waste_percentage = historical_waste.get(
                meal_type,
                0
            )

        else:

            waste_percentage = current_waste_percentage


        # =================================================
        # DAY OF WEEK
        # =================================================

        day_of_week = (
            meal_date.weekday() + 1
        ) % 7


        # =================================================
        # MEAL TYPE NUMBER
        # =================================================

        meal_type_number = meal_mapping.get(
            meal_type,
            0
        )


        # =================================================
        # ML INPUT
        # =================================================

        input_data = pd.DataFrame([{

            "meal_type_encoded":
                meal_type_number,

            "day_of_week":
                day_of_week,

            "waste_percentage":
                waste_percentage

        }])


        # =================================================
        # ML PREDICTION
        # =================================================

        ml_prediction = model.predict(
            input_data
        )[0]

        ml_prediction = max(
            0,
            round(ml_prediction)
        )


        # =================================================
        # HISTORICAL AVERAGE
        # =================================================

        historical_average = round(
            historical_demand.get(
                meal_type,
                0
            )
        )


        # =================================================
        # COMBINE HISTORICAL + ML
        # =================================================

        if historical_average > 0:

            demand_base = (
                historical_average * 0.70
            ) + (
                ml_prediction * 0.30
            )

        else:

            demand_base = ml_prediction


        # =================================================
        # CURRENT BOOKINGS ADJUSTMENT
        # =================================================

        booking_adjustment = min(
            current_bookings * 0.25,
            3
        )


        predicted_quantity = round(
            demand_base
            +
            booking_adjustment
        )


        # =================================================
        # SMALL BUFFER
        # =================================================

        predicted_quantity += 1


        # =================================================
        # FOOD WASTE ADJUSTMENT
        # =================================================

        if waste_percentage >= 20:

            predicted_quantity = round(
                predicted_quantity * 0.85
            )

        elif waste_percentage >= 10:

            predicted_quantity = round(
                predicted_quantity * 0.90
            )


        # =================================================
        # NEVER GO BELOW CURRENT BOOKINGS
        # =================================================

        predicted_quantity = max(
            predicted_quantity,
            current_bookings
        )


        # =================================================
        # REALISTIC LIMIT
        # =================================================

        if historical_average > 0:

            realistic_limit = math.ceil(
                historical_average * 1.25
            )

        else:

            realistic_limit = (
                current_bookings + 5
            )


        # =================================================
        # NEVER EXCEED TOTAL STUDENTS
        # =================================================

        realistic_limit = min(
            realistic_limit,
            total_students
        )


        # =================================================
        # FINAL RECOMMENDATION
        # =================================================

        predicted_quantity = min(
            predicted_quantity,
            realistic_limit
        )


        # =================================================
        # FINAL SAFETY CHECK
        # =================================================

        predicted_quantity = max(
            predicted_quantity,
            current_bookings
        )


        # =================================================
        # STORE RESULT
        # =================================================

        predictions.append({

            "meal_id":
                meal_id,

            "meal_name":
                meal_name,

            "meal_type":
                meal_type,

            "meal_date":
                str(meal_date),

            "current_bookings":
                current_bookings,

            "historical_average":
                historical_average,

            "ml_prediction":
                ml_prediction,

            "waste_percentage":
                round(
                    waste_percentage,
                    2
                ),

            "predicted_quantity":
                predicted_quantity

        })


    # =====================================================
    # RETURN RESULTS
    # =====================================================

    return predictions