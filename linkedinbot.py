from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from time import time
start_time = time()
from warnings import warn
import pandas as pd
import re
import job_filter
import hash
import collect_data as cd

# url = "https://www.linkedin.com/jobs/search/?f_E=2%2C1&f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD"
url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=102095887&keywords=software%20engineer&location=California%2C%20United%20States&sortBy=DD&redirect=false&position=1&pageNum=0&f_TP=1%2C2'
no_of_jobs = 25
# getVars = {'f_E' : '2', 'f_TPR' : 'r86400', 'geoId': '102095887', 'keywords' : job_title, 'location' : location, 'sortBy': 'DD'}
# url = ('https://www.linkedin.com/jobs/search/?' + urllib.parse.urlencode(getVars))
# print("url: ", url)
driver = webdriver.Chrome('/Users/anna/projects-sept2020/linkedin-bot/chromedriver')
driver.get(url)
# sleep(3)
# action = ActionChains(driver)
# i = 2
# while i <= (no_of_jobs/25): 
#     driver.find_element_by_xpath('/html/body/main/div/section/button').click()
#     i += 1
#     sleep(5)
# # parsing the visible webpage


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
flag=1
while flag==1:

  driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

  try:
   wait = WebDriverWait(driver, 10)

   new_height = wait.until(infinite_scroll( last_height))
   last_height = new_height

  except:
      print("End of page reached")
      flag = 0

pageSource = driver.page_source
lxml_soup = BeautifulSoup(pageSource, 'lxml')

job_container = lxml_soup.find('ul', class_ = 'jobs-search__results-list')
print('Job postings found: {}', len(job_container))

cd.collect_data(driver, job_container)
