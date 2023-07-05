import random
import requests
import urllib.parse
from urllib.parse import urlencode
from typing import List
from enum import Enum
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd

JOB_SEARCH_PAGE_LIMIT = 3


class Level(Enum):
    INTERNSHIP = "1"
    ENTRY = "2"
    MIDANDSENIOR = "3"
    DIRECTOR = "4"

class JobPostedTimeRange(Enum):
    DAY = "day"
    WEEK = "week"
    ANY = ""

class NoListingException(Exception):
    pass 


class JobScraper:
    def __init__(self, keywords: str, is_remote: bool, level: Level, job_posted_time: str, location: str = "", geo_id: str = "") -> None:
        self.keywords = keywords
        self.is_remote = is_remote
        self.level = level
        self.location = location
        self.geo_id = geo_id
        self.job_posted_time = job_posted_time
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
        self.jobs = []
        self.job_ids = []

    def scrape_jobs(self) -> List[dict]:
        try:
            job_ids = self.get_job_ids(JOB_SEARCH_PAGE_LIMIT)
            jobs = self.get_jobs_descriptions(job_ids)
            self.get_recruiters(jobs)
            return jobs
        except requests.exceptions.RequestException as e:
            print(f"Error with request occurred while scraping jobs: {e}")
        except Exception as e:
            print(f"Error Scarping Jobs: {e}")

    def get_job_ids(self, job_listing_count) -> List[str]:
            for page in range(job_listing_count):
                
                job_search_url = self._construct_job_listings_url() + f"&start={page}"
                res = self._get_request(job_search_url)
                job_soup = BeautifulSoup(res.text, 'html.parser')
                job_listings = job_soup.find_all("li")
                
                if not job_listings: 
                    continue 
                
                self.job_ids.append(
                    job_listings[page].find("div", {"class": "base-card"}).get("data-entity-urn").split(":")[3]
                )
                
            if not self.job_ids:
                raise NoListingException("No Listing Found")
            
            return self.job_ids
            


    def get_jobs_descriptions(self, job_ids: List[str]) -> List[dict]:
        target_url = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/"
        for job_id in job_ids:
            resp = self._get_request(target_url + f"{job_id}")
            soup = BeautifulSoup(resp.text, "html.parser")
            job_listing = {}
            try:
                job_listing["company"] = soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
            except:
                job_listing["company"] = None
            try:
                job_listing["job-title"] = self._construct_link(
                    soup.find("div",{"class":"top-card-layout__entity-info"}).find("a")["href"], 
                    soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
                    )
            except:
                job_listing["job-title"] = None
            try:
                job_listing["level"] = soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
            except:
                job_listing["level"] = None
            self.jobs.append(job_listing)
        return self.jobs

    def get_recruiters(self, job_listings: List[dict]) -> None:
        for job in job_listings:
            # Google doesn't like scraping so we're putting a timeout on each call 
            results = search(f"Recruiter {job['company']} linkedin", sleep_interval=random.randint(3, 10), num_results=3)
            job["recruiters"] = "\n".join([recruiter_url for recruiter_url in results])
            
    def _construct_link(self, link, text):
        return f'=HYPERLINK("{link}", "{text}")'

    def _construct_job_listings_url(self) -> str:
        base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        params = {
            "keywords": self.keywords,
            "location": self.location,
            "geoId": self.geo_id,
            "f_TPR": self._get_time_range(),
            "f_JT": "F",
            "f_WT": "2" if self.is_remote else "",
            "distance": 25,
            "pageNum": "0",
            "position": "1",
        }
        encoded_params = urlencode(params)
        return base_url + "?" + encoded_params

    def _get_time_range(self) -> str:
        if self.job_posted_time == "week":
            return "r604800"
        elif self.job_posted_time == "day":
            return "r86400"
        else:
            return ""

    def _get_request(self, url: str) -> requests.Response:
        res = requests.get(url=url, headers=self.headers)
        res.raise_for_status()
        return res
    
        


if __name__ == '__main__':
    # Job title, Is remote, level, and "day"
    job_scraper = JobScraper("software engineer", True, Level.MIDANDSENIOR, JobPostedTimeRange.DAY)
    jobs = job_scraper.scrape_jobs()
    
    # Move this to another class 
    df = pd.DataFrame(jobs)
    df.to_csv('linkedinjobs.csv', mode='a', header=False, index=False, encoding='utf-8')

