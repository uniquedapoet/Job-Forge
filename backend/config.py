# Stores API keys, database URL, JWT secrets.
import os

# Define the SQLite database URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USER_DATABASE_PATH = os.path.join(BASE_DIR, 'data/db', "users.db")
USER_DATABASE_URL = f"{USER_DATABASE_PATH}"

RESUME_DATABASE_PATH = os.path.join(BASE_DIR, 'data/db', "resume.db")
RESUME_DATABASE_URL = f"{USER_DATABASE_PATH}"

