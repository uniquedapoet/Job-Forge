import uuid
import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from db import UserEngine, UserSession, Base
from models.users import User
from models.savedJobs import SavedJob
from sqlalchemy.exc import IntegrityError

engine = UserEngine
Session = UserSession


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False, unique=True)
    filename = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())
    resume_text = Column(String, nullable=True)
    user = relationship("User", back_populates="resumes")

    @staticmethod
    def insert_resume(user_id: int, uploaded_file: str) -> None:
        from services.resume_scraper import extract_text_from_pdf
        try:
            session = Session()

            existing_resume = session.query(Resume).filter(
                Resume.user_id == user_id).first()

            if existing_resume:
                existing_file = os.path.join(
                    'backend/data/resumes', existing_resume.filename)

                session.delete(existing_resume)
                session.commit()

                try:
                    os.remove(existing_file)
                    print(
                        f" Removed existing resume file: {existing_resume.filename}"
                    )
                except FileNotFoundError:
                    print(
                        f"File not found: {existing_resume.filename}, skipping deletion."
                    )
                except Exception as e:
                    print(f"Error removing existing file: {e}")

            unique_filename = f"{user_id}_{uuid.uuid4().hex}.pdf"
            file_path = os.path.join('backend/data/resumes', unique_filename)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            file_url = f"/download/{unique_filename}"

            resume_text = extract_text_from_pdf(file_path)

            new_resume = Resume(
                user_id=user_id,
                filename=unique_filename,
                file_url=file_url,
                resume_text=resume_text

            )

            session.add(new_resume)
            session.commit()
            print("Inserted new resume")

        except Exception as e:
            print(f"Error inserting resume: {e}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def get_resumes_by_user_id(user_id: int) -> dict:
        session = Session()
        resume = session.query(Resume).filter(
            Resume.user_id == user_id).first()
        session.close()
        try:
            resume = {
                column.key: getattr(resume, column.key)
                for column in Resume.__table__.columns
            }
            return resume
        except Exception:
            return "No Resume Found"

    @staticmethod
    def clear_resumes() -> None:
        session = Session()
        session.query(Resume).delete()
        session.commit()
        session.close()
        print("✅ Resumes table cleared.")

    @staticmethod
    def allowed_file(filename) -> bool:
        """Check if the uploaded file has an allowed extension."""
        return '.' in filename and (
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @staticmethod
    def delete_resume(user_id):
        session = Session()
        try:
            session.query(Resume).filter(Resume.user_id == user_id).delete()

            return f"Resume Deleted for user ({user_id})"
        except Exception as e:

            return f'Error deleting resume for user ({e})'

    @staticmethod
    def add_resume_text(user_id, resume_text):
        session = Session()
        try:
            saved_resume = session.query(Resume).filter(
                Resume.user_id == user_id).first()

            if not saved_resume:
                return f'No Saved Resume for user {user_id}'

            saved_resume.resume_text = resume_text
            session.commit()

        except IntegrityError as e:
            return f'Error Adding Resume Text {e}'

        finally:
            session.close()

    @staticmethod
    def get_resume_text(user_id):
        session = Session()
        try:
            resume = session.query(Resume).filter(
                Resume.user_id == user_id).first()

            if not resume:
                return f'Error Finding Resume for User: {user_id}'

            session.commit()
            return resume.resume_text
        except IntegrityError as e:
            return f'Error Finding Resume For User: {user_id}, {e}'

        finally:
            session.close()
