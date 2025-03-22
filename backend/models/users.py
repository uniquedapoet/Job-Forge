import os
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
import pandas as pd
from db import UserEngine, UserSession, Base


engine = UserEngine
Session = UserSession


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    city = Column(String)
    zipcode = Column(String)
    job_titles = Column(String)

    resumes = relationship(
        "Resume", back_populates="user", cascade="all, delete")
    saved_jobs = relationship(
        "SavedJob", back_populates="user", cascade="all, delete")

    @staticmethod
    def create_tables():
        print("Ensuring tables exist in the database...")
        Base.metadata.create_all(UserEngine, checkfirst=True)
        print("Tables verified!")

    @staticmethod
    def register(user_data):
        try:
            session = Session()
            new_user = User(**user_data)
            session.add(new_user)
            session.commit()
            print("Inserted user")
        except Exception as e:
            print(f"Error inserting user: {e}")
            session.rollback()

        finally:
            session.close()

    @staticmethod
    def from_csv(csv_path):
        session = Session()
        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found at {csv_path}")
            return

        user_data = pd.read_csv(csv_path, dtype={
            "username": str, "email": str, "password": str,
            "first_name": str, "last_name": str, "phone": str,
            "city": str, "zipcode": str, "job_titles": str
        })

        for _, row in user_data.iterrows():
            user = User(**row.to_dict())
            session.add(user)

        session.commit()
        session.close()
        print("User data loaded successfully!")

    @staticmethod
    def users(test=False):
        session = Session()
        users = session.query(User).all()
        if test:
            for user in users:
                print(user.__dict__)
        session.close()

        return users

    @staticmethod
    def user(user_id: int):
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        user = {
            column.key: getattr(user, column.key)
            for column in User.__table__.columns
        }
        return user