import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dbConnection import jobUrl_collection




# enable headless mode in Selenium
options = Options()
#options.add_argument('--headless=new')

driver = webdriver.Chrome(
    options=options,
    # other properties...
)

for page in range(1, 101):

    driver.get(f'https://www.avito.ru/perm/vakansii?p={page}')

    # scraping logic...

    soup = BeautifulSoup(driver.page_source, 'lxml')

    jobs = soup.find_all('a', {'itemprop': 'url'})


    jobs = set(jobs)

    for job in jobs:
        jobUrl_collection.insert_one({
            "jobName": job.text,
            "jobUrl": job['href']
        })
    print(f"Current page is:{page}")
    # input("************\nWaiting for input to continue\n************\nPress enter...")

    print("Scraping...")




driver.quit()







