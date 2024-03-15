import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from dbConnection import jobs_collection




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

    jobBlocks = soup.find_all('div', {'data-marker':'item'})

    for jobBlock in jobBlocks:
        job = jobBlock.find_next('a', {'itemprop': 'url', 'data-marker':'item-title'})
        blockLines = jobBlock.find_all_next('div',{'data-marker': "item-line"})

        if blockLines[0].text == "Компания":
            fieldOfExp = blockLines[1].text
        else:
            fieldOfExp = blockLines[0].text

        salary = jobBlock.find_next('meta', {"itemprop": "price"})

        jobs_collection.insert_one({
            "jobName": job['title'],
            "jobUrl": job['href'],
            "fieldOfExp": fieldOfExp,
            "salary": int(salary['content'])
        })





    print(f"Current page is:{page}")
    # input("************\nWaiting for input to continue\n************\nPress enter...")

    print("Scraping...")




driver.quit()







