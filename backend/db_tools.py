import sqlite3
from config import USER_DATABASE_URL, RESUME_DATABASE_URL, JOBS_DATABASE_URL
import us 
import textblob


def correct_spelling(text):
    """Corrects spelling errors in a given text."""
    corrected_text = textblob.TextBlob(text).correct()
    return str(corrected_text)


def state_abbreviations(state_name):
    state = us.states.lookup(state_name)
    return state.abbr if state else state_name


def get_user_by_id(user_id):
    """Fetches a single users data by User ID."""
    conn = sqlite3.connect(USER_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    column_names = [desc[0] for desc in cursor.description]

    conn.close()

    return dict(zip(column_names, user)) if user else None


def get_resumes_by_user_id(user_id):
    """Fetches all resumes for a given user ID."""
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes WHERE user_id = ?", (user_id,))
    resumes = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    conn.close()

    return [dict(zip(column_names, resume)) for resume in resumes]


def get_job(job_id):   
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchall()
    conn.close()

    if job is None:
        return None 

    columns = [desc[0] for desc in cursor.description]  
    job_dict = dict(zip(columns, job))  

    return job_dict



