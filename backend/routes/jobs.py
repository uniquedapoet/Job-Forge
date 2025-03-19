# Scrapes job descriptions from URLs.
# Stores job applications in the database.import os
import sqlite3
import pandas as pd
from config import JOBS_DATABASE_URL
import os


def create_jobs_db():
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
    """Validates and inserts jobs into the database using sqlite3."""
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    expected_columns = ['id', 'site', 'job_url', 'job_url_direct', 'title',
                        'company', 'location', 'date_posted', 'job_type', 'salary_source',
                        'interval', 'min_amount', 'max_amount', 'currency', 'is_remote',
                        'job_level', 'job_function', 'listing_type', 'emails', 'description',
                        'company_industry', 'company_url', 'company_logo', 'company_url_direct',
                        'company_addresses', 'company_num_employees', 'company_revenue',
                        'company_description']

    try:
        # ✅ If job_data is a DataFrame, drop duplicates and iterate over each row
        if isinstance(job_data, pd.DataFrame):
            job_data = job_data.drop_duplicates(subset=["id"])  # Remove duplicate job_ids
            for _, row in job_data.iterrows():
                validate_and_insert_jobs(row.to_dict())  # Convert row to dict and process
            return

        # ✅ If job_data is a Series (single row), convert to dict
        if isinstance(job_data, pd.Series):
            job_data = job_data.to_dict()

        job_id = job_data.get("id")

        # ✅ Fetch all existing job IDs and store them in a set for quick lookup
        cursor.execute("SELECT job_id FROM jobs")
        existing_jobs = {row[0] for row in cursor.fetchall() if row[0]}  # Remove empty job IDs

        if job_id in existing_jobs:
            print(f"🔄 Job {job_id} already exists in the database. Skipping insertion.")
            return

        print(f"🔍 Inserting job: {job_id}")

        # ✅ Ensure only the required columns are inserted
        filtered_job_data = {key: job_data.get(key, "") for key in expected_columns}

        # ✅ Use INSERT OR IGNORE to avoid duplicate errors
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
        print(f"✅ Inserted job: {job_id}")

    except sqlite3.IntegrityError as e:
        print(f"❌ IntegrityError: Job {job_id} could not be inserted: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    finally:
        conn.close()


# def validate_and_insert_jobs(job_data: dict):
#     """Validates and inserts a job into the database using sqlite3."""
#     conn = sqlite3.connect(JOBS_DATABASE_URL)
#     cursor = conn.cursor()

#     # print(type(job_data))

#     # Ensure all 28 fields have values by replacing NaN/None with an empty string
#     expected_columns = ['job_id', 'site', 'job_url', 'job_url_direct', 'title',
#                         'company', 'location', 'date_posted', 'job_type', 'salary_source',
#                         'interval', 'min_amount', 'max_amount', 'currency', 'is_remote',
#                         'job_level', 'job_function', 'listing_type', 'emails', 'description',
#                         'company_industry', 'company_url', 'company_logo', 'company_url_direct',
#                         'company_addresses', 'company_num_employees', 'company_revenue',
#                         'company_description']

#     try:
#         job_id = job_data["id"]

#         # Check if the job already exists
#         cursor.execute("SELECT job_id FROM jobs WHERE job_id = ?", (job_id,))
#         existing_job = cursor.fetchone()

#         if existing_job:
#             print(f"🔄 Job {job_id} already exists, skipping insertion.")
#             return
        
#         print(f"🔍 Inserting job: {job_id}")

#         # Ensure only the required columns are inserted
#         filtered_job_data = {key: job_data[key]
#                              for key in expected_columns if key in job_data}

#         cursor.execute("""
#         INSERT INTO jobs (
#             job_id, site, job_url, job_url_direct, title, company, location, date_posted, job_type, 
#             salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, 
#             job_function, listing_type, emails, description, company_industry, company_url, 
#             company_logo, company_url_direct, company_addresses, company_num_employees, 
#             company_revenue, company_description
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, tuple(filtered_job_data.values()))

#         conn.commit()
#         print(f"✅ Inserted job: {job_data['job_id']}")

#     except sqlite3.IntegrityError as e:
#         print(f"❌ Error inserting job {job_data['job_id']}: {e}")

#     except Exception as e:
#         print(f"❌ Unexpected error: {e}")

#     finally:
#         conn.close()


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
        quotechar='"',
        escapechar="\\",
        engine="python"
    )

    for _, row in job_data.iterrows():
        validate_and_insert_jobs(row.to_dict())

    print("Jobs data loaded successfully!")


def test_job_data():
    """Fetches and prints user data from the database."""
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE id = 1734")
    jobs = cursor.fetchall()

    conn.close()

    for job in jobs:
        print(job)



if __name__ == "__main__":
    pass
