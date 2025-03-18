import os
import sqlite3
import pandas as pd
from config import USER_DATABASE_URL


def create_users_table():
    """Creates the users table in SQLite."""
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

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
    print("Users table created successfully!")


def create_saved_jobs_table():
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
                   """)
    conn.commit()
    conn.close()


def validate_and_insert_user(user_data):
    """Validates and inserts a user into the database using sqlite3."""
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, first_name, last_name, phone, city, zipcode, job_titles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data["username"],
            user_data["email"],
            user_data["password"],  # Should be hashed before storing
            user_data["first_name"],
            user_data["last_name"],
            user_data.get("phone"),
            user_data.get("city"),
            user_data.get("zipcode"),
            user_data.get("job_titles"),
        ))

        conn.commit()
        print(f"Inserted user: {user_data['username']}")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting user {user_data['username']}: {e}")

    finally:
        conn.close()


def user_csv_to_db(csv_path):
    """Loads user data from CSV and inserts it into SQLite."""
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
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    for user in users:
        print(user)


if __name__ == "__main__":
    pass
