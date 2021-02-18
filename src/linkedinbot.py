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

def launch_driver(driver, url):
    # url = "https://www.linkedin.com/jobs/search/?f_E=2%2C1&f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD"
    # url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD&redirect=false&position=1&pageNum=0&f_TP=1%2C2'
    # getVars = {'f_E' : '2', 'f_TPR' : 'r86400', 'geoId': '102095887', 'keywords' : job_title, 'location' : location, 'sortBy': 'DD'}
    # url = ('https://www.linkedin.com/jobs/search/?' + urllib.parse.urlencode(getVars))
    # print("url: ", url)
    # options = Options()
    # options.add_argument('--headless')    # without opening Chrome window

    # driver = webdriver.Chrome('src/chromedriver', options=options)
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
    flag = 1
    while flag == 1:
      driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
      try:
        wait = WebDriverWait(driver, 10)
        new_height = wait.until(infinite_scroll(last_height))
        last_height = new_height
      except:
          print("End of page reached")
          flag = 0

    # pageSource = driver.page_source
    lxml_soup = BeautifulSoup(driver.page_source, 'lxml')

    job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
    print('Job postings found:', len(job_container))
    return job_container


def extract_data(driver, job_container):
    ''' 
    driver -> web driver, Chrome
    job_container -> a web container with all job postings
    Extracts all jobs postings and theri attributes from the job container
    Returns a list of Job_Posting objects 
    '''
    if len(job_container) == 0:
        raise ValueError('Job container is empty. To proceed, it must contain at least one item.')
    
    job_postings = []


    for i in range(1, len(job_container)+1):
        # print(i)
        # job_id = i.find('a', href=True)['href']
        # job_id = re.findall(r'(?!-)([0-9]*)(?=\?)',job_id)[0]
        # # job_postings.append(job_id)
        # print(f'job_id = {job_id}')

        try:
            job_xpath = f'/html/body/main/div/section/ul/li[{i}]/img'
            driver.find_element_by_xpath(job_xpath).click()
            sleep(3)
            job = Job_Posting

            job.title = driver.find_element_by_class_name('topcard__title').text

            job.link = driver.find_element_by_xpath('/html/body/main/section/div[2]/section/div[1]/div[1]/a').get_attribute('href')

            job.company = driver.find_element_by_class_name('topcard__flavor').text

            job.location = driver.find_element_by_class_name('topcard__flavor--bullet').text

            job.level = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/ul/li[1]/span').text

            job.description = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/div/section/div').text

            job.date_posted = date.today().strftime("%m/%d/%y")

            job_postings.append(job)

        except Exception as e:
            print('Runtime error while processing a job posting')
            print(e.args)
            print(e.with_traceback)

    return job_postings


if __name__ == "__main__":
    url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD&redirect=false&position=1&pageNum=0&f_TP=1%2C2'
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('src/chromedriver', options=options)

    job_container = launch_driver(driver, url)
    job_postings = extract_data(driver, job_container)
    
    store_data(job_postings)

