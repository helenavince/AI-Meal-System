
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

# Find the project's root folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file
load_dotenv(PROJECT_ROOT / ".env")

connection = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "smart_mess"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT", "5432")
)

print("Database connected successfully!")

