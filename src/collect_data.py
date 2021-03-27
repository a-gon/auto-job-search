import re
from time import sleep
from datetime import date
import job_filter as f
import hash as h
from os.path import isfile
import data_store as ds
from job_posting_class import Job_Posting


def store_data(job_list):
    """ Applies filters and stores job postings in a database

    job_list - a list of Job_Posting objects
    avoids saving duplicate job postings into the database by hashing job_description 
    creates the database if it does not exist yet
    return: None
    """

    if not job_list:
        raise ValueError('Job list is empty. To proceed, it must contain at least one item.')
    
    if not isfile('data/visited_jobs.db'):
        ds.create_db()

    accepted, not_accepted = 0, 0

    for job in job_list:
        job.hash = h.get_hash(job.description)
        if h.is_seen(job.hash):
            not_accepted += 1
            continue
        elif f.accepted_title(job.title) and f.accepted_level(job.level) and f.accepted_description(job.description):
            job.accepted = True
            ds.insert_job(job)
            accepted += 1
        else:
            job.accepted = False
            ds.insert_job(job)
            not_accepted += 1
    print(f'Jobs accepted: {accepted}\nJobs not accepted: {not_accepted}') 
