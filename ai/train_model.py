import os
import psycopg2
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor


# =========================================================
# DATABASE CONNECTION
# =========================================================

connection = psycopg2.connect(
    host="localhost",
    database="smart_mess",
    user="postgres",
    password="helena@2006",
    port="5432"
)

print("Database connected successfully!")


# =========================================================
# GET TRAINING DATA
# =========================================================
# A meal is used for AI training only when:
# 1. It has completed bookings
# 2. It has food-waste data
#
# This prevents an upcoming meal with 0 completed bookings
# from being incorrectly treated as zero demand.


query = """
SELECT
    m.meal_id,
    m.meal_type,
    m.meal_date,

    EXTRACT(DOW FROM m.meal_date)::INT AS day_of_week,

    COUNT(
        CASE
            WHEN b.status = 'COMPLETED'
            THEN b.booking_id
        END
    )::INT AS booking_count,

    fw.prepared_quantity,
    fw.consumed_quantity,
    fw.waste_quantity

FROM meals m

INNER JOIN food_waste fw
    ON m.meal_id = fw.meal_id

INNER JOIN bookings b
    ON m.meal_id = b.meal_id
    AND b.status = 'COMPLETED'

GROUP BY
    m.meal_id,
    m.meal_type,
    m.meal_date,
    fw.prepared_quantity,
    fw.consumed_quantity,
    fw.waste_quantity

ORDER BY m.meal_date;
"""


df = pd.read_sql(query, connection)

connection.close()


# =========================================================
# DISPLAY TRAINING DATA
# =========================================================

print("\nHistorical training data:")

print(df)

print("\nTraining rows:", len(df))


# =========================================================
# CHECK DATA
# =========================================================

if len(df) == 0:

    print("\nERROR: No completed meal data found.")

    print(
        "At least one meal must have COMPLETED bookings "
        "and food-waste data."
    )

    exit()


# =========================================================
# CALCULATE WASTE PERCENTAGE
# =========================================================

df["waste_percentage"] = (
    df["waste_quantity"] /
    df["prepared_quantity"]
) * 100


# =========================================================
# MEAL TYPE ENCODING
# =========================================================

meal_type_mapping = {

    "Breakfast": 0,

    "Lunch": 1,

    "Snacks": 2,

    "Dinner": 3

}


df["meal_type_encoded"] = df["meal_type"].map(
    meal_type_mapping
)


# =========================================================
# REMOVE UNKNOWN MEAL TYPES
# =========================================================

df = df.dropna(
    subset=["meal_type_encoded"]
)


# =========================================================
# TRAINING FEATURES
# =========================================================

X = df[
    [
        "meal_type_encoded",
        "day_of_week",
        "waste_percentage"
    ]
]


# =========================================================
# TARGET
# =========================================================

y = df["booking_count"]


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    max_depth=5,

    min_samples_leaf=1

)


# =========================================================
# TRAIN MODEL
# =========================================================

model.fit(X, y)


# =========================================================
# SAVE MODEL
# =========================================================

project_root = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


model_path = os.path.join(
    project_root,
    "meal_demand_model.pkl"
)


joblib.dump(
    model,
    model_path
)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n===================================")

print("AI MODEL TRAINED SUCCESSFULLY!")

print("===================================")

print("\nTraining rows:", len(df))


print("\nFeatures used:")

print("1. Meal type")

print("2. Day of week")

print("3. Food waste percentage")


print("\nTarget:")

print("Expected booking demand")


# =========================================================
# HISTORICAL DEMAND
# =========================================================

print("\nHistorical booking demand:")


for meal_type in meal_type_mapping.keys():

    meal_data = df[
        df["meal_type"] == meal_type
    ]

    if len(meal_data) > 0:

        average = meal_data[
            "booking_count"
        ].mean()

        print(
            f"{meal_type}: {average:.2f} students"
        )


# =========================================================
# MODEL LOCATION
# =========================================================

print("\nModel saved at:")

print(model_path)


print("\n===================================")