# Scrapes job postings using BeautifulSoup & Selenium.
# https://github.com/Bunsly/JobSpy/tree/main

import csv
import os
from jobspy import scrape_jobs

# get path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
data_dir = os.path.join(backend_dir, "data")
file_path = os.path.join(data_dir, "jobs.csv")


def getJobsData(job_title: str, location: str):
    jobs = scrape_jobs(
    site_name=['indeed'], # others may require proxies: "linkedin", "zip_recruiter", "glassdoor", "google"
    search_term=job_title,
    location=location,
    results_wanted=20,
    hours_old=72,
    country_indeed='USA'
    
    # linkedin_fetch_description=True # gets more info such as description, direct job url (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    )
    print(f"Found {len(jobs)} jobs")
    return jobs

jobs = getJobsData("Data Scientist", "Denver, CO")

jobs.to_csv(file_path, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel



