import sqlite3
from config import USER_DATABASE_URL

def get_user_by_id(user_id):
        """Fetches a single users data by User ID."""
        conn = sqlite3.connect(USER_DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        conn.close()

        return dict(zip(column_names, user)) if user else None