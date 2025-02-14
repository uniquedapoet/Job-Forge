import sqlite3
import os
import pandas as pd
from config import USER_DATABASE_URL
from models import User  # Import your SQLAlchemy model
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQLAlchemy setup
engine = create_engine(f"sqlite:///{USER_DATABASE_URL}")  # Change to PostgreSQL URL if needed
Session = sessionmaker(bind=engine)
session = Session()

def create_users_table():
    os.makedirs(os.path.dirname(USER_DATABASE_URL), exist_ok=True)

    # Connect to SQLite database (or create if it doesn't exist)
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    # Create the users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT,
        city TEXT,
        zipcode TEXT,
        job_titles TEXT
    );
    """)

    conn.commit()
    conn.close()

    print("Database and table created successfully!")


def validate_and_insert_user(user_data):
    """Validates and inserts a user into the database using SQLAlchemy."""
    try:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],  # Hash this before storing
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data.get("phone"),
            city=user_data.get("city"),
            zipcode=user_data.get("zipcode"),
            job_titles=user_data.get("job_titles"),
        )
        session.add(user)
        session.commit()
        print(f"Inserted user: {user.username}")
    except Exception as e:
        session.rollback()
        print(f"Error inserting user {user_data.get('username')}: {e}")


def user_csv_to_db(csv_path):
    """Loads user data from CSV and validates it with the SQLAlchemy model before insertion."""
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    user_data = pd.read_csv(csv_path, dtype={
        "username": str, "email": str, "password": str,
        "first_name": str, "last_name": str, "phone": str,
        "city": str, "zipcode": str, "job_titles": str
    })

    for _, row in user_data.iterrows():
        validate_and_insert_user(row.to_dict())

    print("User data loaded successfully!")


def test_user_data():
    """Fetches and prints user data from the database."""
    with sqlite3.connect(USER_DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

    for user in users:
        print(user)


if __name__ == "__main__":
    create_users_table()
    user_csv_to_db("./backend/data/csvs/user_data.csv")
    test_user_data()
