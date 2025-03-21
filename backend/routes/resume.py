import uuid
from config import RESUME_DATABASE_URL
import sqlite3
import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import UserEngine, UserSession

Base = declarative_base()
engine = UserEngine
Session = UserSession

class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="resumes")

    def __init__(self, user_id, filename, file_url):
        self.user_id = user_id
        self.filename = filename
        self.file_url = file_url

    @staticmethod
    def create_tables():
        print("🔧 Ensuring tables exist in the database...")
        Base.metadata.create_all(UserEngine, checkfirst=True)
        
        print("✅ Tables verified!")

    @staticmethod
    def insert_resume(user_id: int, uploaded_file):
        try:
            session = Session()
                
            _ = session.query(Resume).filter(Resume.user_id == user_id).delete()
            session.commit()

            # Generate a unique filename
            unique_filename = f"{user_id}_{uuid.uuid4().hex}.pdf"
            file_path = os.path.join('backend/data/resumes', unique_filename)

            # Save the file locally
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Store the file URL
            file_url = f"/download/{unique_filename}"  # API path for downloading

            new_resume = Resume(user_id=user_id,
                                filename=unique_filename,
                                file_url=file_url)
            session.add(new_resume)
            session.commit()
            print("Inserted resume")
        except Exception as e:
            print(f"Error inserting resume: {e}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get_resumes_by_user_id(user_id):
        session = Session()
        resumes = session.query(Resume).filter(Resume.user_id == user_id).all()
        session.close()
        return resumes
    
    @staticmethod
    def clear_resumes():
        session = Session()
        session.query(Resume).delete()
        session.commit()
        session.close()
        print("✅ Resumes table cleared.")


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
    print('======================', RESUME_DATABASE_URL)
    if not os.path.exists(RESUME_DATABASE_URL):
        print(
            f"❌ Database file {RESUME_DATABASE_URL} does not exist. Creating...")
        create_resumes_table()
    
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT filename FROM resumes WHERE user_id = ?", (user_id,))
        existing_resume = cursor.fetchone()

        if existing_resume:
            existing_file = os.path.join('backend/data/resumes', existing_resume[0])
            try:
                os.remove(existing_file)
                print(f"✅ Removed existing resume file: {existing_resume[0]}")
            except Exception as e:
                print(f"❌ Error removing existing file: {e}")

        cursor.execute("DELETE FROM resumes WHERE user_id = ?", (user_id,))
        conn.commit()

        # Generate a unique filename
        unique_filename = f"{user_id}_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join('backend/data/resumes', unique_filename)

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
        print(
            f"Inserted resume for user_id: {user_id}, File: {unique_filename}")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting resume for user_id {user_id}: {e}")

    finally:
        conn.close()


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and (
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def clear_resumes_table():
    """Clears the resumes table in SQLite."""
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resumes")
    conn.commit()
    conn.close()
    print("✅ Resumes table cleared.")
