from sqlalchemy import create_engine, text

db_path = "/Users/eduardobenjamin/Desktop/Repos/Job-Forge/backend/data/database/users.db"
engine = create_engine(f"sqlite:///{db_path}", echo=True)

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM users LIMIT 5;"))
    for row in result:
        print(row)
