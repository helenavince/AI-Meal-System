"""
=============================================================================
Synthetic Dataset Generator for Smart Mess AI Demand Prediction
=============================================================================
This module generates a realistic, statistically grounded synthetic dataset
simulating 180 days of college hostel mess attendance, bookings, and food waste.
Each record is explicitly documented as synthetic data generated for modeling.

Features generated:
- date: YYYY-MM-DD
- meal_type: Breakfast, Lunch, Dinner
- day_of_week: Monday, Tuesday, ... Sunday
- day_of_week_num: 0-6
- is_weekend: 0 (weekday) or 1 (weekend)
- is_exam_period: 0 or 1 (e.g. higher mess presence, altered study patterns)
- is_special_menu: 0 or 1 (e.g. Sunday feast, festival meal)
- booking_count: Pre-booked student slots
- prev_week_attendance: Attendance for same meal type 7 days prior
- prev_day_same_meal: Attendance yesterday for same meal
- actual_attendance: True student turn-up (Target Variable for Demand Prediction)
- actual_prepared: Quantity kitchen prepared based on heuristic buffer
- actual_served: Min(actual_attendance, actual_prepared)
- leftover_portions: actual_prepared - actual_served
- waste_percentage: (leftover_portions / actual_prepared) * 100
=============================================================================
"""

import os
import random
import datetime
import pandas as pd
import numpy as np

def generate_mess_history(days: int = 180, output_path: str = None) -> pd.DataFrame:
    """Generates synthetic historical college mess data for training."""
    random.seed(42)
    np.random.seed(42)
    
    start_date = datetime.date(2026, 4, 1)
    records = []
    
    # Meal baseline configs (total registered students in hostel ~ 450)
    TOTAL_STUDENTS = 450
    
    meal_configs = {
        'Breakfast': {
            'base_booking': 300,
            'weekend_booking_factor': 0.70,  # Many students sleep in on weekends
            'attendance_rate': 0.88,         # ~88% of booked students show up
            'walk_in_rate': 0.04,            # ~4% unbooked walk-ins
            'dishes': ['Idli', 'Sambar', 'Coconut Chutney', 'Medu Vada']
        },
        'Lunch': {
            'base_booking': 410,
            'weekend_booking_factor': 0.95,  # Weekend lunch is popular
            'attendance_rate': 0.93,
            'walk_in_rate': 0.03,
            'dishes': ['Steamed Rice', 'Sambar', 'Vegetable Poriyal', 'Curd', 'Rasam']
        },
        'Dinner': {
            'base_booking': 390,
            'weekend_booking_factor': 0.85,  # Weekend outings reduce dinner
            'attendance_rate': 0.91,
            'walk_in_rate': 0.05,
            'dishes': ['Wheat Chapati', 'Mixed Vegetable Curry', 'Dal Tadka', 'Jeera Rice']
        }
    }
    
    # We will track attendance in memory to build realistic lag features
    history_by_meal = {'Breakfast': [], 'Lunch': [], 'Dinner': []}
    
    for day_idx in range(days):
        current_date = start_date + datetime.timedelta(days=day_idx)
        date_str = current_date.isoformat()
        day_of_week = current_date.strftime('%A')
        day_num = current_date.weekday()
        is_weekend = 1 if day_num in [5, 6] else 0
        
        # Exam periods: simulate 2 exam windows in 180 days (days 40-55 and 130-145)
        is_exam = 1 if (40 <= day_idx <= 55) or (130 <= day_idx <= 145) else 0
        
        for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
            cfg = meal_configs[meal_type]
            
            # Special menu on Sundays or mid-week festivals
            is_special = 1 if (day_num == 6 and meal_type == 'Lunch') or (day_idx % 28 == 0) else 0
            
            # Booking calculations
            weekend_mod = cfg['weekend_booking_factor'] if is_weekend else 1.0
            exam_mod = 1.05 if (is_exam and meal_type != 'Breakfast') else (0.92 if is_exam else 1.0)
            special_mod = 1.10 if is_special else 1.0
            
            mean_booking = cfg['base_booking'] * weekend_mod * exam_mod * special_mod
            noise_booking = np.random.normal(0, 12)
            booking_count = int(np.clip(mean_booking + noise_booking, 120, TOTAL_STUDENTS))
            
            # Lag features from history
            past_attendances = history_by_meal[meal_type]
            if len(past_attendances) >= 7:
                prev_week_att = past_attendances[-7]
            elif len(past_attendances) > 0:
                prev_week_att = past_attendances[-1]
            else:
                prev_week_att = int(booking_count * cfg['attendance_rate'])
                
            prev_day_att = past_attendances[-1] if len(past_attendances) > 0 else int(booking_count * cfg['attendance_rate'])
            
            # Attendance generation: function of bookings + day factors + noise
            turnout_rate = cfg['attendance_rate'] + np.random.normal(0, 0.025)
            turnout_rate = np.clip(turnout_rate, 0.75, 0.98)
            
            booked_turnout = int(booking_count * turnout_rate)
            walk_ins = int(booking_count * cfg['walk_in_rate'] + np.random.normal(0, 4))
            walk_ins = max(0, walk_ins)
            
            actual_attendance = int(np.clip(booked_turnout + walk_ins, 100, TOTAL_STUDENTS))
            history_by_meal[meal_type].append(actual_attendance)
            
            # Mess preparation: Traditionally prepared with a naive 12-15% over-margin over bookings
            naive_margin = 1.12 + np.random.uniform(-0.03, 0.04)
            actual_prepared = int(round(booking_count * naive_margin))
            # Ensure prepared is at least close to attendance
            actual_prepared = max(actual_prepared, actual_attendance + random.randint(5, 25))
            
            actual_served = min(actual_attendance, actual_prepared)
            leftover = max(0, actual_prepared - actual_served)
            waste_pct = round((leftover / actual_prepared) * 100, 2) if actual_prepared > 0 else 0.0
            
            records.append({
                'dataset_type': 'SYNTHETIC_TRAINING_RECORD',
                'date': date_str,
                'meal_type': meal_type,
                'day_of_week': day_of_week,
                'day_of_week_num': day_num,
                'is_weekend': is_weekend,
                'is_exam_period': is_exam,
                'is_special_menu': is_special,
                'booking_count': booking_count,
                'prev_week_attendance': prev_week_att,
                'prev_day_attendance': prev_day_att,
                'actual_attendance': actual_attendance,
                'actual_prepared': actual_prepared,
                'actual_served': actual_served,
                'leftover_portions': leftover,
                'waste_percentage': waste_pct
            })
            
    df = pd.DataFrame(records)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} synthetic records saved to: {output_path}")
        
    return df

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    csv_file = os.path.join(data_dir, 'synthetic_mess_history.csv')
    df = generate_mess_history(days=180, output_path=csv_file)
    print("Dataset sample head:")
    print(df[['date', 'meal_type', 'booking_count', 'actual_attendance', 'leftover_portions', 'waste_percentage']].head())
