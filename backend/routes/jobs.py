# Scrapes job descriptions from URLs.
# Stores job applications in the database.import os
import sqlite3
import pandas as pd
from config import JOBS_DATABASE_URL
import os


def create_jobs_table():
    """Creates the jobs table in SQLite."""
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT UNIQUE NOT NULL,
        site TEXT,
        job_url TEXT,
        job_url_direct TEXT,
        title TEXT,
        company TEXT,
        location TEXT,
        date_posted TEXT,
        job_type TEXT,
        salary_source TEXT,
        interval TEXT,
        min_amount FLOAT,
        max_amount FLOAT,
        currency TEXT,
        is_remote BOOLEAN,
        job_level TEXT,
        job_function TEXT,
        listing_type TEXT,
        emails TEXT,
        description TEXT,
        company_industry TEXT,
        company_url TEXT,
        company_logo TEXT,
        company_url_direct TEXT,
        company_addresses TEXT,
        company_num_employees TEXT,
        company_revenue TEXT,
        company_description TEXT
     );
    """)

    conn.commit()
    conn.close()
    print("Users table created successfully!")



def validate_and_insert_jobs(job_data):
    """Validates and inserts a job into the database using sqlite3."""
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    # Debugging: Print keys before inserting
    print(f"🔹 Job Data Keys: {list(job_data.keys())}")
    print(f"🔹 Number of Keys: {len(job_data.keys())}")

    # Ensure all 28 fields have values by replacing NaN/None with an empty string
    expected_columns = ['job_id', 'site', 'job_url', 'job_url_direct', 'title', 
                        'company', 'location', 'date_posted', 'job_type', 'salary_source',
                        'interval', 'min_amount', 'max_amount', 'currency', 'is_remote', 
                        'job_level', 'job_function', 'listing_type', 'emails', 'description',
                        'company_industry', 'company_url', 'company_logo', 'company_url_direct',
                        'company_addresses', 'company_num_employees', 'company_revenue', 
                        'company_description']

    extra_columns = [key for key in job_data.keys() if key not in expected_columns]

    print(f"🔹 Expected Columns: {len(expected_columns)}, Found: {len(job_data.keys())}")
    if extra_columns:
        print(f"❌ Extra Columns Detected: {extra_columns}")

     # Extract values for insertion
    job_values = list(job_data.values())

    # Debugging: Print values before inserting
    print(f"🔍 Job Data Values (Before Insert): {job_values}")
    print(f"🔍 Number of Values: {len(job_values)}")

    try:
        # Ensure only the required columns are inserted
        filtered_job_data = {key: job_data[key] for key in expected_columns if key in job_data}

        cursor.execute("""
        INSERT INTO jobs (
            job_id, site, job_url, job_url_direct, title, company, location, date_posted, job_type, 
            salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, 
            job_function, listing_type, emails, description, company_industry, company_url, 
            company_logo, company_url_direct, company_addresses, company_num_employees, 
            company_revenue, company_description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(filtered_job_data.values()))

        conn.commit()
        print(f"✅ Inserted job: {job_data['job_id']}")

    except sqlite3.IntegrityError as e:
        print(f"❌ Error inserting job {job_data['job_id']}: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    finally:
        conn.close()


def jobs_csv_to_db(csv_path):
    """Loads user data from CSV and inserts it into SQLite."""
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    job_data = pd.read_csv(csv_path, dtype={
        "job_id": str, "site": str, "job_url": str, "job_url_direct": str, "title": str, "company": str,
        "location": str, "date_posted": str, "job_type": str, "salary_source": str, "interval": str,
        "min_amount": float, "max_amount": float, "currency": str, "is_remote": int, "job_level": str,
        "job_function": str, "listing_type": str, "emails": str, "description": str, "company_industry": str,
        "company_url": str, "company_logo": str, "company_url_direct": str, "company_addresses": str,
        "company_num_employees": str, "company_revenue": str, "company_description": str
    },
    # Ensures multiline fields (like job descriptions) are properly read
    quotechar='"',
    escapechar="\\",
    engine="python"
    )

    print(f"✅ Data has {len(job_data)} fields, expected 27.")
    print(f"✅ Job data keys: {list(job_data.keys())}")

    for _, row in job_data.iterrows():
        validate_and_insert_jobs(row.to_dict())

    print("Jobs data loaded successfully!")


def test_job_data():
    """Fetches and prints user data from the database."""
    conn=sqlite3.connect(JOBS_DATABASE_URL)
    cursor=conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    jobs=cursor.fetchall()

    conn.close()

    for job in jobs:
        print(job)


if __name__ == "__main__":
    test_job_data()
