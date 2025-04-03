from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    ForeignKey,
    func,
    Float
)
from sqlalchemy.orm import relationship
from db import UserEngine, UserSession, Base
from typing import List


engine = UserEngine
Session = UserSession


class SavedJob(Base):
    __tablename__ = 'saved_jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, nullable=False)
    job_score = Column(Float)
    saved_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="saved_jobs")

    @staticmethod
    def save(user_id, job_id, job_score=0) -> None:
        session = Session()
        try:
            saved_job = SavedJob(
                user_id=user_id, job_id=job_id, job_score=job_score)

            session.add(saved_job)
            session.commit()
            print(f"Inserted saved job: {job_id}")

        except Exception as e:
            print(f"Error inserting saved job {job_id}: {e}")
            session.rollback()

        finally:
            session.close()

    @staticmethod
    def get_job_score(user_id: int, job_id: int) -> int:
        session = Session()
        try:
            session.commit()
            job_score = session.query(SavedJob.job_score).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
            return job_score[0] if job_score else 0
        except Exception as e:
            print(f"Error getting job score: {e}")
            return None

        finally:
            session.close()

    @staticmethod
    def get_saved_jobs(user_id: int) -> List[dict]:
        session = Session()
        try:
            saved_jobs = session.query(SavedJob).filter(
                SavedJob.user_id == user_id).all()

            saved_jobs = [{column.key: getattr(
                saved_job, column.key) for column in SavedJob.__table__.columns
            } for saved_job in saved_jobs]

            return saved_jobs

        except Exception as e:
            print(f"Error getting saved jobs: {e}")
            return None

        finally:
            session.close()

    @staticmethod
    def remove_saved_job(user_id: int, job_id: int) -> None:
        session = Session()
        try:
            saved_job = session.query(SavedJob).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
            session.delete(saved_job)
            session.commit()

        except Exception as e:
            print(f"Error removing saved job: {e}")

        finally:
            session.close()

    @staticmethod
    def remove_saved_jobs(user_id: int) -> None:
        session = Session()
        try:
            session.query(SavedJob).filter(
                SavedJob.user_id == user_id).delete()
            session.commit()

        except Exception as e:
            print(f"Error removing job scores: {e}")

        finally:
            session.close()
