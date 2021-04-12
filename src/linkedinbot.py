from os import system
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import time
from time import sleep
from datetime import datetime
import sys
import urllib.parse as urlparse
from urllib.parse import urlencode
import logging
logging.basicConfig(filename='extraction.log',level=logging.ERROR)

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

    # TODO: check if there's a button "Show more" and click it

    lxml_soup = BeautifulSoup(driver.page_source, 'lxml')

    job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
    print('Job postings found:', len(job_container))
    return job_container


def extract_data(driver, job_container, test=False):
    """ Extract data from job_container and return a list of Job_Posting objects

    Arguments:
    driver -- a web driver (Chrome)
    job_container -- an html element on the page that contains all job postings
    """
    if len(job_container) == 0:
        raise ValueError('Job container is empty. To proceed, it must contain at least one item.')
    
    job_list = []
    errors = 0
    num_jobs = len(job_container)+1 if not test else 6
    for i in range(1, num_jobs):
        try:
            job_xpath = f'/html/body/main/div/section[2]/ul/li[{i}]/img'
            driver.find_element_by_xpath(job_xpath).click()
            
            sleep(3)    # wait for all components to get loaded after clicking
            job = Job_Posting(
                hash = '',
                title = driver.find_element_by_class_name('topcard__title').text,
                link = driver.find_element_by_xpath("//a[@data-tracking-control-name='public_jobs_topcard_title']").get_attribute('href'),
                company = driver.find_element_by_class_name('topcard__flavor').text,
                location = driver.find_element_by_class_name('topcard__flavor--bullet').text,
                level = driver.find_element_by_class_name('job-criteria__text--criteria').text,
                description = "",
                date_posted = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                accepted = False
            )
            driver.find_element_by_class_name('show-more-less-html__button--more').click()
            sleep(1)
            job.description = driver.find_element_by_class_name('show-more-less-html__markup').text

            job_list.append(job)

        except Exception:
            errors += 1
            logging.exception('Runtime error while processing a job posting')
    print(f'Errors encountered: {errors}')
    return job_list

def create_url(url, params):
    """ Create a full url from the short url and search parameters
    """
    param_dict = {'keywords': params[0], 'location': params[1], 'sortBy': 'R'}
    full_url = url + urlencode(param_dict)
    return full_url

if __name__ == "__main__":
    """ Extract arguments first, if any """
    url = ''
    if len(sys.argv) > 1:
        SEARCH_POSITION = sys.argv[1]
        SEARCH_LOCATION = sys.argv[2]
        url = create_url('https://www.linkedin.com/jobs/search/?', [SEARCH_POSITION, SEARCH_LOCATION])
    else:
        """ Copy and paste url - this one enables only job postings from certain companies within the past week """
        url = 'https://www.linkedin.com/jobs/search/?f_C=1815218%2C2620735%2C162479%2C96622%2C7594728%2C206993%2C3185%2C22688%2C3477522%2C10667%2C1337%2C1666%2C1586%2C1035%2C1441&geoId=103644278&keywords=software%20engineer&location=United%20States&f_TPR=r604800&position=1&pageNum=0'


    """ Set HEADLESS = True to avoid opening Chrome browser window """
    HEADLESS = True        
    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")

    """ Set driver with options and launch the driver to get the large container with all job postings on the page"""
    driver = webdriver.Chrome(options=options)

    job_container = launch_driver(driver, url)

    """ Enable or disable TEST - if True, extracts only 5 jobs to test """
    TEST = True 
    """ Extract all jobs from the job container """
    job_list = extract_data(driver, job_container, TEST)
    
    """ Process (apply filters) and store all data """
    store_data(job_list)
    to_csv(True)        # output accepted jobs to csv file
    to_csv(False)       # output not accepted jobs into csv file, uncomment if needed
    
    driver.quit()       # close all windows, release resources



