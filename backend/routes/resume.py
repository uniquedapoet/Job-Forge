import uuid
from config import RESUME_DATABASE_URL
import sqlite3
import os

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


def create_resumes_table():
    """Creates the resumes table in SQLite and ensures the database file is generated."""
    try:
        # Ensure the directory for the database exists
        db_directory = os.path.dirname(RESUME_DATABASE_URL)
        if not os.path.exists(db_directory):
            os.makedirs(db_directory, exist_ok=True)
            print(f"✅ Created database directory: {db_directory}")

        # Connect to SQLite (creates file if it doesn't exist)
        conn = sqlite3.connect(RESUME_DATABASE_URL)
        cursor = conn.cursor()

        # Create table if it doesn't exist
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
        print(f"✅ Database file created at: {RESUME_DATABASE_URL}")

        # Check if the database file exists now
        if os.path.exists(RESUME_DATABASE_URL):
            print(f"✅ Database {RESUME_DATABASE_URL} successfully created.")
        else:
            print(f"❌ Database file {RESUME_DATABASE_URL} was not created.")

    except Exception as e:
        print(f"❌ Error creating database: {e}")


def validate_and_insert_resume(user_id, uploaded_file):
    """Generates filename and file URL, then inserts into the database."""
    print('======================',RESUME_DATABASE_URL)
    if not os.path.exists(RESUME_DATABASE_URL):
        print(f"❌ Database file {RESUME_DATABASE_URL} does not exist. Creating...")
        create_resumes_table()

    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT filename FROM resumes WHERE user_id = ?", (user_id,))
        existing_resume = cursor.fetchone()

        if existing_resume:
            existing_file = os.path.join('data/resumes',existing_resume[0])
            if os.path.exists(existing_file):
                os.remove(existing_file)
                print(f"Removed existing resume file: {existing_resume}")

            cursor.execute("DELETE FROM resumes WHERE user_id = ?", (user_id,))                                       
                
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


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and (
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        )