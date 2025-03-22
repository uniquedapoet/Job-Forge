from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.declarative import declarative_base

# Create a declarative base
Base = declarative_base()

# Get absolute path for the SQLite database
user_db_path = os.path.abspath("backend/data/database/users.db")

# Ensure the directory exists before creating the database
db_dir = os.path.dirname(user_db_path)
os.makedirs(db_dir, exist_ok=True)

# Create engine with correct SQLite settings
UserEngine = create_engine(f"sqlite:///{user_db_path}", connect_args={"check_same_thread": False}, echo=True)
UserSession = sessionmaker(bind=UserEngine)

import models  

# ✅ Create tables after models are imported
Base.metadata.create_all(UserEngine, checkfirst=True)
