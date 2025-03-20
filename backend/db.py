from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get absolute path for the SQLite database
db_path = os.path.abspath("backend/data/database/users.db")

# Ensure the directory exists before creating the database
db_dir = os.path.dirname(db_path)
os.makedirs(db_dir, exist_ok=True)

# Create engine with correct SQLite settings
UserEngine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False}, echo=True)
UserSession = sessionmaker(bind=UserEngine)

print(f"✅ Database path: {db_path}")
