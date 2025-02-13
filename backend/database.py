import sqlite3
from config import USER_DATABASE_URL
import pandas as pd
import os
# Establishes PostgreSQL connection using SQLAlchemy.
# Defines a session for interacting with the database.

# Create SQLAlchemy instance


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


def user_csv_to_db(csv_path):
    # Load user data from CSV
    user_data = pd.read_csv(csv_path)

    # Connect to SQLite database
    conn = sqlite3.connect(USER_DATABASE_URL)

    # Insert user data into the users table
    user_data.to_sql(
        "users", conn, if_exists="replace", index=False
        )
    
    conn.commit()
    conn.close()

    print("User data loaded successfully!")


def test_user_data():
    # Connect to SQLite database
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    # Query the users table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Print the user data
    for user in users:
        print(user)

    conn.close()


if __name__ == "__main__":
    user_csv_to_db("./backend/data/user_data.csv")
    test_user_data()