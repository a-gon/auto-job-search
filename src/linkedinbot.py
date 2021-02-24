from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import time
from time import sleep
from datetime import date
import re
import traceback

from job_posting_class import Job_Posting
start_time = time()
from collect_data import store_data
from data_store import to_csv

def launch_driver(driver, url):
    """ Launch a web driver that will go to url, scroll to end of page 
    and return a web container with all job postings

    Arguments:
    driver -- a web driver (Chrome)
    url -- page that web driver launches and collects info from
    """
    driver.get(url)
    if not driver:
        raise RuntimeError('Driver object is incorrect.')

    class infinite_scroll(object):
      def __init__(self, last):
        self.last = last
      def __call__(self, driver):
        new = driver.execute_script('return document.body.scrollHeight')  
        if new > self.last:
            return new
        else:
            return False
    last_height = driver.execute_script('return document.body.scrollHeight')
    endOfPage = False
    while endOfPage == False:
      driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
      try:
        wait = WebDriverWait(driver, 10)
        new_height = wait.until(infinite_scroll(last_height))
        last_height = new_height
      except:
          print("End of page reached")
          endOfPage = True

    lxml_soup = BeautifulSoup(driver.page_source, 'lxml')

    job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
    print('Job postings found:', len(job_container))
    # print(job_container)
    return job_container


def extract_data(driver, job_container):
    """ Extract data from job_container and return a list of Job_Posting objects

    Arguments:
    driver -- a web driver (Chrome)
    job_container -- an html element on the page that contains all job postings
    """
    if len(job_container) == 0:
        raise ValueError('Job container is empty. To proceed, it must contain at least one item.')
    
    job_list = []

    for i in range(1, len(job_container)+1):
        try:
            job_xpath = f'/html/body/main/div/section[2]/ul/li[{i}]/img'
            driver.find_element_by_xpath(job_xpath).click()
            sleep(3)    # so that driver does not flood the page with requests
            job = Job_Posting(
                hash = '',
                title = driver.find_element_by_class_name('topcard__title').text,
                link = driver.find_element_by_xpath("//a[@data-tracking-control-name='public_jobs_topcard_title']").get_attribute('href'),
                company = driver.find_element_by_class_name('topcard__flavor').text,
                location = driver.find_element_by_class_name('topcard__flavor--bullet').text,
                level = driver.find_element_by_class_name('job-criteria__text--criteria').text,
                description = driver.find_element_by_class_name('description__text--rich').text,
                date_posted = date.today().strftime("%m/%d/%y"),
                accepted = 0
            )

            job_list.append(job)

        except Exception:
            print(f'Runtime error while processing a job posting')
            print(traceback.format_exc())

    return job_list


if __name__ == "__main__":
    # SEARCH_POSITION
    # SEARCH_LOCATION
    HEADLESS = True    # TODO: add this as kwargs
    url = 'https://www.linkedin.com/jobs/search/?f_TP=1%2C2&f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=R'
    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    driver = webdriver.Chrome('src/chromedriver', options=options)

    job_container = launch_driver(driver, url)
    job_list = extract_data(driver, job_container)
    
    store_data(job_list)
    to_csv(True)        # output accepted jobs to csv file
    to_csv(False)       # output not accepted jobs into csv file
    driver.quit()       # closes all windows, release resources



