import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from time import time
import pandas as pd
import job_filter as f
import hash as h
from os import path
import shelve




def collect_data(driver, job_container):
    print('Getting information about {} jobs.'.format(len(job_container)))
    job_postings = []
    # setting up list for job information
    JOBID = []
    TITLE = []
    COMPANY = []
    LOCATION = []
    JOB_DESC = []
    LEVEL = []
    LINK = []

    # get all job postings on the loaded page
    for job in job_container:
        
        job_id = job.find('a', href=True)['href']
        job_id = re.findall(r'(?!-)([0-9]*)(?=\?)',job_id)[0]
        job_postings.append(job_id)

    # for loop for job description and criterias
    title, link, company, location, job_id, level = None, None, None, None, None, None
    for x in range(1,len(job_postings)+1):
        
        # clicking on different job containers to view information about the job
        job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
        driver.find_element_by_xpath(job_xpath).click()
        sleep(3)

        title = driver.find_element_by_class_name('topcard__title').text

        # apply link
        link = driver.find_element_by_xpath('/html/body/main/section/div[2]/section/div[1]/div[1]/a').get_attribute('href')

        company = driver.find_element_by_class_name('topcard__flavor').text

        location = driver.find_element_by_class_name('topcard__flavor--bullet').text

        job_id = driver.find_elements_by_id('jobId')
        
        level = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/ul/li[1]/span').text

        job_desc = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/div/section/div').text
        job_hash = h.get_hash(job_desc)

        # seniority = job_criteria_container.find('span', class_='job-criteria__text job-criteria__text--criteria').text
        if f.accepted_title(title) and f.acceted_level(level) and h.is_new(job_hash) and f.accepted_description(job_desc):
            TITLE.append(title)
            COMPANY.append(company)
            LOCATION.append(location)
            JOBID.append(job_id)
            LINK.append(link)
            LEVEL.append(level)
            JOB_DESC.append(job_desc)
            h.add_to_db(job_hash)        
        

        # # job criteria container below the description
        # job_criteria_container = lxml_soup.find('ul', class_ = 'job-criteria__list')
        # all_job_criterias = job_criteria_container.find_all("span", class_='job-criteria__text job-criteria__text--criteria')
        
        x = x+1


    # print('JOBID: {}',len(JOBID))   
    # print('Company: {}',len(COMPANY))
    # print('Title: {}',len(TITLE))
    # print('Location: {}',len(LOCATION))
    # print('Descr: {}',len(JOB_DESC))
    # print('Level: {}',len(LEVEL))
    # print('Link: {}',len(LINK))

    job_data = pd.DataFrame({
    'Job ID': JOBID,
    'Link' : LINK,
    'Company': COMPANY,
    'Title': TITLE,
    'Location': LOCATION,
    'Level': LEVEL,
    'Description': JOB_DESC,
    })

    # cleaning description column
    job_data['Description'] = job_data['Description'].str.replace('\n',' ')

    print(job_data.info())

    if not path.exists("collected_data.csv"):
        job_data.to_csv('collected_data.csv', index=0)
    else:
        job_data.to_csv('collected_data.csv', mode='a', header=False, index=0)



# with shelve.open('jobs') as jobs:
#     print('Hashed jobs:  ', len(jobs['applied']))
