import hashlib
import shelve
from os import path

def get_hash(job_description):
    job_description = job_description.encode('utf-8')
    # print(job_description)
    hash_object = hashlib.md5(job_description.lower())
    return hash_object.hexdigest()

def is_new(hash):
    if not path.exists("jobs"):
        return True
    with shelve.open('jobs') as jobs:
        if hash in jobs['applied']:
            print('Exists in db')
            return False
    return True

def add_to_db(hash):
    with shelve.open('jobs') as jobs:
        if not jobs:
            jobs['applied'] = {hash}
        else:
            jobs['applied'].add(hash)
    print('Added to database')

