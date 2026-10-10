"""
=============================================================================
Machine Learning Model Training Pipeline for Smart Mess Demand Prediction
=============================================================================
Trains a scikit-learn regressor on historical/synthetic mess demand data.
Computes real evaluation metrics (MAE, RMSE, R²) without hardcoding.
Persists model pipeline and metadata for the FastAPI inference service.
=============================================================================
"""

import os
import json
import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from .data_generator import generate_mess_history

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODEL_PATH = os.path.join(BASE_DIR, 'demand_model.joblib')
METRICS_PATH = os.path.join(BASE_DIR, 'model_metrics.json')

def train_and_evaluate():
    os.makedirs(DATA_DIR, exist_ok=True)
    csv_file = os.path.join(DATA_DIR, 'synthetic_mess_history.csv')
    
    if not os.path.exists(csv_file):
        print("Historical dataset not found. Generating 180 days synthetic dataset...")
        df = generate_mess_history(days=180, output_path=csv_file)
    else:
        df = pd.read_csv(csv_file)
        print(f"Loaded existing dataset with {len(df)} records from {csv_file}")

    feature_cols_num = [
        'booking_count',
        'prev_week_attendance',
        'prev_day_attendance',
        'is_weekend',
        'is_exam_period',
        'is_special_menu',
        'day_of_week_num'
    ]
    feature_cols_cat = ['meal_type']
    target_col = 'actual_attendance'

    X = df[feature_cols_num + feature_cols_cat]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, shuffle=True
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), feature_cols_num),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), feature_cols_cat)
        ]
    )

    # Ridge regressor with preprocessor pipeline for explainable coefficients
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ])

    print("Fitting Ridge regression model on training partition...")
    model.fit(X_train, y_train)

    # Evaluate predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_mae = float(mean_absolute_error(y_train, y_pred_train))
    test_mae = float(mean_absolute_error(y_test, y_pred_test))
    test_rmse = float(np.sqrt(mean_squared_error(y_test, y_pred_test)))
    test_r2 = float(r2_score(y_test, y_pred_test))

    print(f"Model Training Results:")
    print(f" - Train MAE: {train_mae:.2f} portions")
    print(f" - Test MAE:  {test_mae:.2f} portions")
    print(f" - Test RMSE: {test_rmse:.2f} portions")
    print(f" - Test R²:   {test_r2:.4f}")

    # Extract feature names & coefficients for transparent explainability
    ohe_categories = model.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(feature_cols_cat)
    all_feature_names = feature_cols_num + list(ohe_categories)
    coefficients = model.named_steps['regressor'].coef_
    feature_importances = {name: round(float(coef), 4) for name, coef in zip(all_feature_names, coefficients)}

    # Save model binary
    joblib.dump(model, MODEL_PATH)
    print(f"Saved trained model artifact to: {MODEL_PATH}")

    # Save evaluation summary and metadata
    metadata = {
        "model_name": "SmartMess Demand Regressor",
        "algorithm": "Ridge Regression with Scaled Feature Pipeline",
        "trained_at": datetime.datetime.now().isoformat(),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "train_mae": round(train_mae, 2),
        "test_mae": round(test_mae, 2),
        "test_rmse": round(test_rmse, 2),
        "test_r2": round(test_r2, 4),
        "feature_weights": feature_importances,
        "intercept": round(float(model.named_steps['regressor'].intercept_), 4),
        "dataset_type": "180-Day Statistically Grounded College Mess Dataset (Clearly Labeled Synthetic)",
        "features_used": feature_cols_num + feature_cols_cat
    }

    with open(METRICS_PATH, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved model evaluation metadata to: {METRICS_PATH}")
    return metadata

if __name__ == '__main__':
    train_and_evaluate()
