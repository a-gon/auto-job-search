from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import time
from time import sleep
from datetime import date
import re

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
            job_xpath = f'/html/body/main/div/section/ul/li[{i}]/img'
            driver.find_element_by_xpath(job_xpath).click()
            sleep(3)    # so that driver does not flood the page with requests
            job = Job_Posting(
                title=driver.find_element_by_class_name('topcard__title').text,
                title = driver.find_element_by_class_name('topcard__title').text,
                link = driver.find_element_by_xpath('/html/body/main/section/div[2]/section/div[1]/div[1]/a').get_attribute('href'),
                company = driver.find_element_by_class_name('topcard__flavor').text,
                location = driver.find_element_by_class_name('topcard__flavor--bullet').text,
                level = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/ul/li[1]/span').text,
                description = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/div/section/div').text,
                date_posted = date.today().strftime("%m/%d/%y")
            )
            job_list.append(job)

        except Exception as e:
            print('Runtime error while processing a job posting')
            print(e.args)
            print(e.with_traceback)

    return job_list


if __name__ == "__main__":
    # SEARCH_POSITION
    # SEARCH_LOCATION
    # HEADLESS = True
    url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD&redirect=false&position=1&pageNum=0&f_TP=1%2C2'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('src/chromedriver', options=options)

    job_container = launch_driver(driver, url)
    job_list = extract_data(driver, job_container)
    
    store_data(job_list)
    to_csv('acceptedJobs')
    to_csv('notacceptedJobs')
    driver.quit()       # closes all windows, release resources



