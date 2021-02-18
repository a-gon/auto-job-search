import re
from time import sleep
from datetime import date
import job_filter as f
import hash as h
from os.path import isfile
import data_store as ds

def collect_data(driver, job_container):
    '''
    collect_data function: receives the driver object and a container with job postings,
    visits each job posting and collects the required data
    avoids saving duplicate job postings into the database by hashing the job description 
    creates the database if it does not exist yet
    '''
    if len(job_container) == 0:
        raise ValueError('Job container is empty. To proceed, it must contain at least one item.')
    if not driver:
        raise RuntimeError('Driver object is incorrect.')

    print(f'Getting information about {len(job_container)} jobs.')

    if not isfile('visited_jobs.db'):
        ds.createdb()

    job_postings = []
   
    for job in job_container:
        job_id = job.find('a', href=True)['href']
        job_id = re.findall(r'(?!-)([0-9]*)(?=\?)',job_id)[0]
        job_postings.append(job_id)

    title, date_posted, link, company, location, job_id, level = None, None, None, None, None, None, None
    accepted, not_accepted = 0, 0

    for x in range(1,len(job_postings)+1):
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

            date_posted = date.today().strftime("%m/%d/%y")
        except RuntimeError as e:
            print('Runtime error while processing a job posting')
            print(e.args)
            print(e.with_traceback)

        job_hash = h.get_hash(job_desc)
        # print(job_hash)
        if h.is_in_accepted(job_hash) or h.is_in_notaccepted(job_hash):
            continue
        elif f.accepted_title(title) and f.accepted_level(level) and f.accepted_description(job_desc):
            ds.insert_accepted_job((job_hash, date_posted, title, company, location, level, job_desc, link))
            accepted += 1
        else:
            ds.insert_notaccepted_job((job_hash, date_posted))     
            not_accepted += 1
    print(f'Jobs accepted: {accepted}\nJobs not accepted: {not_accepted}') 
