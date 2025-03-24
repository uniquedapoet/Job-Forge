# Stores API keys, database URL, JWT secrets.
import os

# Define the SQLite database URL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JOBS_DATABASE_PATH = os.path.join(BASE_DIR, 'data/db', "jobs.db")
JOBS_DATABASE_URL = f"{JOBS_DATABASE_PATH}"

