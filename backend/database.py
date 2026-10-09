import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="smart_mess",
    user="postgres",
    password="helena@2006",
    port="5432"
)

print("Database connected successfully!")