from sqlalchemy import create_engine, text

db_path = "/Users/eduardobenjamin/Desktop/Repos/Job-Forge/backend/data/database/users.db"
engine = create_engine(f"sqlite:///{db_path}", echo=True)

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users LIMIT 5;"))
    for row in result:
        print(row)

        
def validate_and_insert_resume(user_id, uploaded_file):
    """Generates filename and file URL, then inserts into the database."""
    print('======================', RESUME_DATABASE_URL)
    if not os.path.exists(RESUME_DATABASE_URL):
        print(
            f"❌ Database file {RESUME_DATABASE_URL} does not exist. Creating...")
        create_resumes_table()
    
    conn = sqlite3.connect(RESUME_DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT filename FROM resumes WHERE user_id = ?", (user_id,))
        existing_resume = cursor.fetchone()

        if existing_resume:
            existing_file = os.path.join('backend/data/resumes', existing_resume[0])
            try:
                os.remove(existing_file)
                print(f"✅ Removed existing resume file: {existing_resume[0]}")
            except Exception as e:
                print(f"❌ Error removing existing file: {e}")

        cursor.execute("DELETE FROM resumes WHERE user_id = ?", (user_id,))
        conn.commit()

        # Generate a unique filename
        unique_filename = f"{user_id}_{uuid.uuid4().hex}.pdf"
        file_path = os.path.join('backend/data/resumes', unique_filename)

        # Save the file locally
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Store the file URL
        file_url = f"/download/{unique_filename}"  # API path for downloading

        # Insert into the database
        cursor.execute("""
        INSERT INTO resumes (user_id, filename, file_url)
        VALUES (?, ?, ?)
        """, (user_id, unique_filename, file_url))

        conn.commit()
        print(
            f"Inserted resume for user_id: {user_id}, File: {unique_filename}")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting resume for user_id {user_id}: {e}")

    finally:
        conn.close()