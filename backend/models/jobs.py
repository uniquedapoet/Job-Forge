# Scrapes job descriptions from URLs.
# Stores job applications in the database.import os
import sqlite3
import pandas as pd
from config import JOBS_DATABASE_URL
import os
from sqlalchemy import (
    desc,
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    or_
)
from db import Base, JobEngine, JobSession
from sqlalchemy.exc import IntegrityError
from datetime import date

Engine = JobEngine
Session = JobSession

#####

# Update the jobs endpoint to ensure that it retrieves jobs from the current day.

#####


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, unique=True, nullable=False)
    site = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    job_url_direct = Column(String, nullable=True)
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    date_posted = Column(Date, nullable=True)
    job_type = Column(String, nullable=True)
    salary_source = Column(String, nullable=True)
    interval = Column(String, nullable=True)
    min_amount = Column(Float, nullable=True)
    max_amount = Column(Float, nullable=True)
    currency = Column(String, nullable=True)
    is_remote = Column(Boolean, nullable=True)
    job_level = Column(String, nullable=True)
    job_function = Column(String, nullable=True)
    listing_type = Column(String, nullable=True)
    emails = Column(String, nullable=True)
    description = Column(String, nullable=True)
    company_industry = Column(String, nullable=True)
    company_url = Column(String, nullable=True)
    company_logo = Column(String, nullable=True)
    company_url_direct = Column(String, nullable=True)
    company_addresses = Column(String, nullable=True)
    company_num_employees = Column(String, nullable=True)
    company_revenue = Column(String, nullable=True)
    company_description = Column(String, nullable=True)

    def create_jobs_db():
        """Creates the jobs table in SQLite."""
        Base.metadata.create_all(Engine)
        print("Jobs table created successfully!")

    @staticmethod
    def jobs():
        session = Session()
        jobs = session.query(Job).all()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_id(job_id: int):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        session.close()

        job = {column: getattr(job, column)
               for column in job.__table__.columns.keys()}

        return job

    @staticmethod
    def jobs_by_job_id(job_id: str):
        session = Session()
        job = session.query(Job).filter(Job.id == job_id).first()
        session.close()

        job = {column: getattr(job, column)
               for column in job.__table__.columns.keys()}

        return job

    @staticmethod
    def jobs_by_title(title):
        session = Session()
        jobs = session.query(Job).filter(
            Job.title.like(f"%{title}%")).order_by(
            desc(Job.date_posted)).all()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_company(company):
        session = Session()
        jobs = session.query(Job).filter(
            Job.company.like(f"%{company}%")).all()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_location(location):
        session = Session()
        jobs = session.query(Job).filter(
            Job.location.like(f"%{location}%")).order_by(
            desc(Job.date_posted)).all().all()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_salary(min_salary, max_salary):
        session = Session()
        jobs = session.query(Job).filter(
            Job.min_amount >= min_salary, Job.max_amount <= max_salary).all()
        session.close()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_remote(remote):
        session = Session()
        jobs = session.query(Job).filter(Job.is_remote == remote).all()
        session.close()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_level(level):
        session = Session()
        jobs = session.query(Job).filter(Job.job_level == level).all()
        session.close()
        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def jobs_by_location_and_title(location, title):
        session = Session()

        title_keywords = title.split()

        # create ilike conditions for each word in the title
        title_filters = [
            Job.title.ilike(f"%{word}%") for word in title_keywords]

        jobs = session.query(Job).filter(Job.location.like(
            f"%{location}%"), or_(*title_filters)).order_by(
                 desc(Job.date_posted)).all()

        session.close()

        job_list = [{column: getattr(
            job, column) for column in job.__table__.columns.keys()
        } for job in jobs]

        return job_list

    @staticmethod
    def description_by_id(job_id):
        session = Session()

        job = session.query(Job).filter(Job.id == job_id).first()
        session.close()

        return job.description


def validate_and_insert_jobs(job_data):
    """Validates and inserts jobs into the database using sqlite3."""
    session = Session()

    expected_columns = ['id', 'site', 'job_url', 'job_url_direct', 'title',
                        'company', 'location', 'date_posted', 'job_type', 'salary_source',
                        'interval', 'min_amount', 'max_amount', 'currency', 'is_remote',
                        'job_level', 'job_function', 'listing_type', 'emails', 'description',
                        'company_industry', 'company_url', 'company_logo', 'company_url_direct',
                        'company_addresses', 'company_num_employees', 'company_revenue',
                        'company_description']

    try:
        #  If job_data is a DataFrame, drop duplicates and iterate over each row
        if isinstance(job_data, pd.DataFrame):
            job_data = job_data.drop_duplicates(
                subset=["id"])  # Remove duplicate job_ids
            for _, row in job_data.iterrows():
                validate_and_insert_jobs(row.to_dict())
            return

        #  If job_data is a Series (single row), convert to dict
        if isinstance(job_data, pd.Series):
            job_data = job_data.to_dict()

        job_id = job_data.get("id")

        existing_job_ids = session.query(Job.job_id).all()
        existing_jobs = {job.job_id for job in existing_job_ids if job.job_id}

        if job_id in existing_jobs:
            print(
                f"🔄 Job {job_id} already exists in the database. Skipping insertion.")
            return

        #  Ensure only the required columns are inserted
        filtered_job_data = {key: job_data.get(
            key, None) for key in expected_columns}
        filtered_job_data['job_id'] = filtered_job_data.pop('id')

        #  Use INSERT OR IGNORE to avoid duplicate errors
        session.add(Job(**filtered_job_data))
        session.commit()

    except IntegrityError as e:
        print(f"❌ IntegrityError: Job {job_id} could not be inserted: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    finally:
        session.close()
