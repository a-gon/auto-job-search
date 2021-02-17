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
import data_store as ds




def collect_data(driver, job_container):
    print('Getting information about {} jobs.'.format(len(job_container)))
    job_postings = []

    # get all job postings on the loaded page
    for job in job_container:
        
        job_id = job.find('a', href=True)['href']
        job_id = re.findall(r'(?!-)([0-9]*)(?=\?)',job_id)[0]
        job_postings.append(job_id)

    title, date_posted, link, company, location, job_id, level = None, None, None, None, None, None, None
    accepted, not_accepted = 0, 0

    for x in range(1,len(job_postings)+1):
        
        # clicking on different job containers to view information about the job
        try:
            job_xpath = '/html/body/main/div/section/ul/li[{}]/img'.format(x)
            driver.find_element_by_xpath(job_xpath).click()
            sleep(3)

            title = driver.find_element_by_class_name('topcard__title').text

            link = driver.find_element_by_xpath('/html/body/main/section/div[2]/section/div[1]/div[1]/a').get_attribute('href')

            company = driver.find_element_by_class_name('topcard__flavor').text

            location = driver.find_element_by_class_name('topcard__flavor--bullet').text

            job_id = driver.find_elements_by_id('jobId')
            
            level = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/ul/li[1]/span').text

            job_desc = driver.find_element_by_xpath('/html/body/main/section/div[2]/section[2]/div/section/div').text

            #  TODO: add date to db
            # date_posted = driver.find_element 
        except Exception:
            print(Exception.args)
            print(Exception.with_traceback)

        job_hash = h.get_hash(job_desc)
        print(job_hash)
        # seniority = job_criteria_container.find('span', class_='job-criteria__text job-criteria__text--criteria').text
        if h.is_in_accepted(job_hash) or h.is_in_notaccepted(job_hash):
            continue
        elif f.accepted_title(title) and f.accepted_level(level) and f.accepted_description(job_desc):
            ds.insert_accepted_job((job_hash, date_posted, title, company, location, level, job_desc, link))
            accepted += 1
        else:
            ds.insert_notaccepted_job((job_hash, date_posted))     
            not_accepted += 1
    print(f'Jobs accepted: {accepted}\nJobs not accepted: {not_accepted}') 
    

