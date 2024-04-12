import random
import time
import datetime

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

def get_num_of_pages(url):

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    pages = soup.find('ul', {'data-marker':"pagination-button"})
    #lastPage = pages.find_all_next('li')[-60]

    lastPage = pages.find_all_next('li')
    # for index, page in enumerate(lastPage):
    #     print(index, page.text)
    hopefullyPages = []
    for stuff in lastPage:
        try:

            hopefullyPages.append(int(stuff.text))
        except ValueError:
            pass

    print(f'Last page is: {hopefullyPages[-1]}')
    return hopefullyPages[-1]


url = 'https://www.avito.ru/perm/vakansii/it_internet_telekom-ASgBAgICAUSOC_SdAQ'

lastPage = get_num_of_pages(url)
# lastPage = 100

newJobs = 0
allDuplicates = 0

for page in range(1, lastPage+1):
    duplicates = 0
    driver.get(url+f'?p={page}')

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

        if jobs_collection.find_one({"jobUrl": job['href']}) is None:
            jobs_collection.insert_one({
                "jobName": job['title'],
                "jobUrl": job['href'],
                "fieldOfExp": fieldOfExp,
                "salary": int(salary['content']),
                "dateOfScraping": datetime.datetime.now().strftime("%x")
            })
            newJobs+=1
        else:
            duplicates+=1






    print(f"Current page is: {page}")
    print(f"duplicates found: {duplicates}")
    allDuplicates+=duplicates
    # input("************\nWaiting for input to continue\n************\nPress enter...")

    print("Scraping...")




driver.quit()

print(f"Program finished\nFound {newJobs} new jobs\nStumbled upon {allDuplicates} duplicates")






