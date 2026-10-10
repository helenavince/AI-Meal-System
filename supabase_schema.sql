-- =========================================================================
-- AI-Powered Smart Mess Meal Pre-Booking & Food Waste Reduction System
-- PostgreSQL / Supabase Database Schema
-- =========================================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Student Profiles
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL DEFAULT 'ECE',
    year_of_study INTEGER NOT NULL DEFAULT 3,
    hostel_block TEXT NOT NULL DEFAULT 'Block B',
    room_number TEXT NOT NULL DEFAULT '304',
    dietary_preference TEXT NOT NULL DEFAULT 'Regular',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Master Meal Menus & Timings
CREATE TABLE IF NOT EXISTS meal_menus (
    id TEXT PRIMARY KEY,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner')),
    timing_label TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    main_items TEXT NOT NULL,
    dishes JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Student Meal Bookings (Strict duplicate prevention per student, date, and meal)
CREATE TABLE IF NOT EXISTS bookings (
    id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    student_name TEXT NOT NULL,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner')),
    status TEXT NOT NULL DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'cancelled', 'attended')),
    booked_at TIMESTAMPTZ DEFAULT NOW(),
    cancelled_at TIMESTAMPTZ,
    CONSTRAINT unique_student_meal_date UNIQUE (student_id, date, meal_type)
);

CREATE INDEX IF NOT EXISTS idx_bookings_date_meal ON bookings(date, meal_type);
CREATE INDEX IF NOT EXISTS idx_bookings_student ON bookings(student_id);

-- 4. Meal Preparation & Actual Serving Logs
CREATE TABLE IF NOT EXISTS meal_preparation_logs (
    id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner')),
    booked_count INTEGER NOT NULL DEFAULT 0 CHECK (booked_count >= 0),
    predicted_demand INTEGER NOT NULL DEFAULT 0 CHECK (predicted_demand >= 0),
    recommended_prepared INTEGER NOT NULL DEFAULT 0 CHECK (recommended_prepared >= 0),
    actual_prepared INTEGER NOT NULL DEFAULT 0 CHECK (actual_prepared >= 0),
    actual_served INTEGER NOT NULL DEFAULT 0 CHECK (actual_served >= 0),
    safety_buffer_pct NUMERIC(4,2) NOT NULL DEFAULT 0.08,
    notes TEXT,
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_prep_log_date_meal UNIQUE (date, meal_type)
);

CREATE INDEX IF NOT EXISTS idx_prep_logs_date ON meal_preparation_logs(date);

-- 5. Dish-wise Waste Tracking
CREATE TABLE IF NOT EXISTS dish_waste_records (
    id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner')),
    dish_name TEXT NOT NULL,
    prepared_portions INTEGER NOT NULL CHECK (prepared_portions >= 0),
    served_portions INTEGER NOT NULL CHECK (served_portions >= 0),
    leftover_portions INTEGER NOT NULL CHECK (leftover_portions >= 0),
    waste_percentage NUMERIC(5,2) NOT NULL DEFAULT 0.00,
    reason_category TEXT DEFAULT 'Standard surplus',
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dish_waste_date ON dish_waste_records(date);
CREATE INDEX IF NOT EXISTS idx_dish_waste_dish ON dish_waste_records(dish_name);

-- 6. Machine Learning Demand Predictions Store
CREATE TABLE IF NOT EXISTS demand_predictions (
    id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('Breakfast', 'Lunch', 'Dinner')),
    day_of_week TEXT NOT NULL,
    booking_count INTEGER NOT NULL DEFAULT 0,
    predicted_attendance INTEGER NOT NULL,
    recommended_portions INTEGER NOT NULL,
    safety_buffer_used NUMERIC(4,2) NOT NULL DEFAULT 0.08,
    confidence_score NUMERIC(4,2) DEFAULT 0.92,
    model_version TEXT NOT NULL DEFAULT 'ridge_regressor_v1.0',
    explanation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_prediction_date_meal UNIQUE (date, meal_type)
);

CREATE INDEX IF NOT EXISTS idx_predictions_date ON demand_predictions(date);

-- 7. Seed Initial Data
INSERT INTO students (id, name, roll_number, email, department, year_of_study, hostel_block, room_number)
VALUES 
    ('std_supriya', 'Supriya', 'ECE2023045', 'supriya.ece@college.edu', 'Electronics & Communication Engineering', 3, 'Block B', '304'),
    ('std_helena', 'Helena Vince', 'ECE2023012', 'helena.ece@college.edu', 'Electronics & Communication Engineering', 3, 'Block A', '201'),
    ('std_rahul', 'Rahul Sharma', 'CSE2023089', 'rahul.cse@college.edu', 'Computer Science & Engineering', 3, 'Block C', '108')
ON CONFLICT (id) DO NOTHING;

INSERT INTO meal_menus (id, meal_type, timing_label, start_time, end_time, main_items, dishes)
VALUES 
    ('menu_breakfast', 'Breakfast', '7:00 AM – 8:45 AM', '07:00', '08:45', 'Idli, Sambar & Chutney', '["Idli", "Sambar", "Coconut Chutney", "Medu Vada"]'::jsonb),
    ('menu_lunch', 'Lunch', '12:15 PM – 1:30 PM', '12:15', '13:30', 'Rice, Sambar, Poriyal & Curd', '["Steamed Rice", "Sambar", "Vegetable Poriyal", "Curd", "Rasam"]'::jsonb),
    ('menu_dinner', 'Dinner', '7:00 PM – 8:45 PM', '19:00', '20:45', 'Chapati & Vegetable Curry', '["Wheat Chapati", "Mixed Vegetable Curry", "Dal Tadka", "Jeera Rice"]'::jsonb)
ON CONFLICT (id) DO NOTHING;
