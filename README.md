# Job Searcher


## Background
Now that I have started to look for a job, I found that the experience of just applying for jobs isn't getting me much response and the best way to a recruiter/ hiring manager. So I created this! 

## Getting Started

* Pull this repo
* Have Python 3.X installed 
* run `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
* update `JOB_SEARCH_PAGE_LIMIT` to your limit 
* update `JobScraper("software engineer", True, Level.MIDANDSENIOR, JobPostedTimeRange.DAY)` geo id, location id can be grab from the linkedin URL when you look at a job. 
* run `python3 job_scrapper.py` in this directory 
* This should populate the rows in the `linkedinjobs.csv` file 
* You can import this file into google sheets for your own tracking 


## Things to note

*  Google/ Linkedin are not fond of web scrapping so use this script at your own risk!
    * Limit the amount of search you do, and how often you use this, (This is just a project for my own curosity not meant for scale)
* Recruiter list might not be what you expect since it's a really simple google search for recruiters at a certain company so the result might not be accurate 


## Road Blocks
1. Linkedin API isn't public which is why I decided to scrape what I can publicly without the need for an linkedin account/ api 
    a. This makes it near impossible for me to get accurate recruiter/ hiring manager data 
2. More to add here when they come up/ if I remember them 
## Roadmaps 

1. Finish up tests for the rest of the functions 
2. Move functions into other classes 
3. Find a better way to do google search (right now it is just looking for recruiters)
4. Use google sheets API to auto append data after each run 
4. Find a reliable way to get recruiters at companies 
5. Get the reruiter emails (or just send emails to email permutations based on the person's name/ company)
6. Auto send emails (have a outreach template and use the google mail)