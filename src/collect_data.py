import re
from time import sleep
from datetime import date
import job_filter as f
import hash as h
from os.path import isfile
import data_store as ds
from job_posting_class import Job_Posting


def store_data(job_list):
    '''
    job_posting -> Job_Posting object
    checks that the job posting has already been seen before
    avoids saving duplicate job postings into the database by hashing the job description 
    creates the database if it does not exist yet
    '''
    if not job_list:
        raise ValueError('Job list is empty. To proceed, it must contain at least one item.')
    
    if not isfile('visited_jobs.db'):
        ds.createdb()

    accepted, not_accepted = 0, 0

    for job in job_list:
        job.hash = h.get_hash(job.description)
        if h.is_seen(job.hash):
            continue
        elif f.accepted_title(job.title) and f.accepted_level(job.level) and f.accepted_description(job.description):
            job.accepted = 1
            ds.insert_job(job)
            accepted += 1
        else:
            job.accepted = 0
            ds.insert_job(job)
            not_accepted += 1
    print(f'Jobs accepted: {accepted}\nJobs not accepted: {not_accepted}') 
