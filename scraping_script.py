from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import time

# Specify the path to the chromedriver executable
# Download chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads
driver_path = '/chromedriver/chromedriver.exe'

# Specify the base URL and the search query
base_url = 'https://www.indeed.com/jobs?q=python&start='

# Initialize the webdriver
s = Service(driver_path)
driver = webdriver.Chrome(service=s)

# Define a function to scrape a single page of job listings
def scrape_page(url):
    driver.get(url)
    time.sleep(5) # wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings = soup.find_all('div', class_='job_seen_beacon')
    job_listings = []

    for listing in listings[1:5]:
        job = {}

        job_title = listing.find('h2', class_='jobTitle')
        job['title'] = job_title.text.strip() if job_title else ""

        job_company = listing.find('span', class_='companyName')
        job['company'] = job_company.text.strip() if job_company else ""

        job_location = listing.find('div', class_='companyLocation')
        job['location'] = job_location.text.strip() if job_location else ""

        job_salary = listing.find('span', class_='estimated-salary')
        job['estimated_salary'] = job_salary.text.strip() if job_salary else ""

        job_snippet = listing.find('div', class_='job-snippet')
        job['job_snippet'] = job_snippet.text.strip() if job_snippet else ""

        job_listings.append(job)
    return job_listings

# Scrape the first four pages of job listings
job_listings = []
for i in range(4):
    url = base_url + str(i*10)
    print('url: ', url)
    job_listings += scrape_page(url)

# Save the job listings to a JSON file
with open('indeed_jobs.json', 'w') as outfile:
    json.dump(job_listings, outfile)

# Quit the webdriver
driver.quit()