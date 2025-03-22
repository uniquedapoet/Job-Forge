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

    # @staticmethod
    # def create_tables():
    #     Base.metadata.create_all(engine, checkfirst=True)

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
            session.commit()
            job_score = session.query(SavedJob.job_score).filter(
                SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
            return job_score[0] if job_score else 0
        except Exception as e:
            print(f"Error getting job score: {e}")
            return None