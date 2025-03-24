import sqlite3
from config import JOBS_DATABASE_URL
import us 


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



