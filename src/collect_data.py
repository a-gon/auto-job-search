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

    for job_posting in job_list:
        job_posting.hash = h.get_hash(job_posting.description)
        # print(job_hash)
        if h.is_in_accepted(job_posting.hash) or h.is_in_notaccepted(job_posting.hash):
            return
        elif f.accepted_title(job_posting.title) and f.accepted_level(job_posting.level) and f.accepted_description(job_posting.description):
            ds.insert_accepted_job((job_posting.hash, job_posting.date_posted, job_posting.title, job_posting.company, job_posting.location, job_posting.level, job_posting.description, job_posting.link))
            accepted += 1
        else:
            ds.insert_notaccepted_job((job_posting.hash, job_posting.date_posted))     
            not_accepted += 1

    print(f'Jobs accepted: {accepted}\nJobs not accepted: {not_accepted}') 
