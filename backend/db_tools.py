import sqlite3
from config import USER_DATABASE_URL, RESUME_DATABASE_URL, JOBS_DATABASE_URL
import us 
from models.users import User
from models.resume import Resume
import textblob


def correct_spelling(text):
    """Corrects spelling errors in a given text."""
    # corrected_text = textblob.TextBlob(text).correct()
    # return str(corrected_text)
    return text


def state_abbreviations(state_name):
    state = us.states.lookup(state_name)
    return state.abbr if state else state_name


def get_job_desc(job_id):
    conn = sqlite3.connect(JOBS_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT description FROM jobs WHERE id = ?", (job_id,))
    # cursor.execute("SELECT * FROM jobs")
    job = cursor.fetchone()
    conn.close()

    return job[0]



