import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    TIMESTAMP,
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import pandas as pd
from db import UserEngine, UserSession

engine = UserEngine
Session = UserSession
Base = declarative_base()


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

    saved_jobs = relationship("SavedJob", back_populates="user")

    @staticmethod
    def create_tables():
        print("🔧 Ensuring tables exist in the database...")
        Base.metadata.create_all(UserEngine, checkfirst=True)
        print("✅ Tables verified!")

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
            user.save(session)

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
        return user


class SavedJob(Base):
    __tablename__ = 'saved_jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, nullable=False)
    job_score = Column(Float)
    saved_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="saved_jobs")

    @staticmethod
    def create_tables():
        Base.metadata.create_all(engine, checkfirst=True)

    def save(self):
        try:
            session = Session()
            session.add(self)
            session.commit()
            print(f"Inserted saved job: {self.job_id}")
        except Exception as e:
            print(f"Error inserting saved job {self.job_id}: {e}")
            session.rollback()

    @staticmethod
    def get_job_score(user_id, job_id):
        session = Session()
        try:
            job_score = session.query(SavedJob.job_score).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
            return job_score[0] if job_score else None
        except Exception as e:
            print(f"Error getting job score: {e}")
            return None
