from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    ForeignKey,
    func,
    Float,
    UniqueConstraint,
    JSON
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from db import UserEngine, UserSession, Base
from typing import List
from db_tools import to_list


engine = UserEngine
Session = UserSession


class SavedJob(Base):
    __tablename__ = 'saved_jobs'
    __table_args__ = (
        UniqueConstraint('user_id', 'job_id', name='uix_user_job'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, nullable=False)
    job_score = Column(Float)
    saved_at = Column(TIMESTAMP, server_default=func.now())
    job_specific_suggestions = Column(JSON, nullable=True)

    user = relationship("User", back_populates="saved_jobs")

    @staticmethod
    def save(user_id, job_id) -> None:
        session = Session()
        try:
            saved_job = SavedJob(
                user_id=user_id, job_id=job_id, job_score=0)

            session.add(saved_job)
            session.commit()
            print(f"Inserted saved job: {job_id}")

        except IntegrityError as e:
            print(f"Error inserting saved job {job_id}: {e}")
            session.rollback()

        finally:
            session.close()

    @staticmethod
    def save_job_score(user_id, job_id, job_score):
        session = Session()
        try:
            saved_job = session.query(SavedJob).filter(
                SavedJob.job_id == job_id, SavedJob.user_id == user_id).first()

            if not saved_job:
                return 'error saving job score', 200

            saved_job.job_score = job_score
            session.commit()

        except IntegrityError as e:
            return f'error saving job score {e}', 400
        
        finally:
            session.close()

    @staticmethod
    def get_job_score(user_id: int, job_id: int) -> int:
        session = Session()
        try:
            job_score = session.query(SavedJob.job_score).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()

            session.commit()
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

            saved_jobs = to_list(saved_jobs, SavedJob)

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

    @staticmethod
    def get_job_specific_suggestions(user_id: int, job_id: int):
        session = Session()
        try:
            saved_job = session.query(SavedJob).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()

            if not saved_job:
                return 'Resume not found for this user.'
            
            saved_job_dict = {
                column.key: getattr(saved_job, column.key)
                for column in SavedJob.__table__.columns
            }
            

            if not saved_job_dict['job_specific_suggestions']:
                from services.suggestions import job_based_suggestions
                try:
                    suggestions = job_based_suggestions(
                        user_id=user_id, job_id=job_id
                        )

                    saved_job.job_specific_suggestions = suggestions

                    session.commit()
                    return suggestions  

                except Exception as e:
                    session.rollback()
                    return f'Error getting job specific suggestions: {e}'
                
            else:
                return saved_job_dict['job_specific_suggestions']

        except Exception as e:
            session.rollback()
            return f'Error getting resume suggestions: {e}'

        finally:
            session.close()
