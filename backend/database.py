import os
import sqlite3
import pandas as pd
from config import USER_DATABASE_URL, RESUME_DATABASE_URL
import uuid

# Ensure database directories exist
os.makedirs(os.path.dirname(USER_DATABASE_URL), exist_ok=True)
os.makedirs(os.path.dirname(RESUME_DATABASE_URL), exist_ok=True)


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


def create_resumes_table():
    """Creates the resumes table in SQLite."""
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        file_url TEXT NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("Resumes table created successfully!")


def validate_and_insert_resume(user_id, uploaded_file):
    """Generates filename and file URL, then inserts into the database."""
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()

    try:
        # Generate a unique filename
        unique_filename = f"{user_id}_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join('data/resumes', unique_filename)

        # Save the file locally
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Store the file URL
        file_url = f"/download/{unique_filename}"  # API path for downloading

        # Insert into the database
        cursor.execute("""
        INSERT INTO resumes (user_id, filename, file_url)
        VALUES (?, ?, ?)
        """, (user_id, unique_filename, file_url))

        conn.commit()
        print(f"Inserted resume for user_id: {user_id}, File: {unique_filename}")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting resume for user_id {user_id}: {e}")

    finally:
        conn.close()

        
if __name__ == "__main__":
    # Setup database tables
    create_users_table()
    create_resumes_table()

    # Load users from CSV
    user_csv_to_db("./backend/data/csvs/user_data.csv")

    # Test user data
    test_user_data()
