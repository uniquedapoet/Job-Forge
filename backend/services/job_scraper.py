# Scrapes job postings using BeautifulSoup & Selenium.
# https://github.com/Bunsly/JobSpy/tree/main
import sys
from jobspy import scrape_jobs


# # get path
# script_dir = os.path.dirname(os.path.abspath(__file__))
# backend_dir = os.path.dirname(script_dir)
# data_dir = os.path.join(backend_dir, "data")
# file_path = os.path.join(data_dir, "jobs.csv")




def get_jobs_data(job_title: str, location: str) -> list:

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
    # print(f"Found {len(jobs)} jobs")
    return jobs

if __name__ == "__main__":
    jobs = get_jobs_data("Data Scientist", "Denver, CO")
    print(jobs)

