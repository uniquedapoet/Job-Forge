import sqlite3
from config import JOBS_DATABASE_URL
import us 


def state_abbreviations(state_name):
    state = us.states.lookup(state_name)
    return state.abbr if state else state_name






