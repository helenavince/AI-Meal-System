CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE meals (
    meal_id SERIAL PRIMARY KEY,
    meal_name VARCHAR(100) NOT NULL,
    meal_type VARCHAR(50) NOT NULL,
    meal_date DATE NOT NULL,
    meal_time TIME NOT NULL
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    meal_id INT REFERENCES meals(meal_id),
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'BOOKED'
);

CREATE TABLE food_waste (
    waste_id SERIAL PRIMARY KEY,
    meal_id INT REFERENCES meals(meal_id),
    prepared_quantity INT NOT NULL,
    consumed_quantity INT NOT NULL,
    waste_quantity INT NOT NULL,
    waste_date DATE DEFAULT CURRENT_DATE
);