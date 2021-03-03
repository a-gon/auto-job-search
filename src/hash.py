import hashlib
import data_store as ds

def get_hash(job_description):
    """ Takes in a text and returns a hash key """

    job_description = job_description.encode('utf-8')
    hash_object = hashlib.md5(job_description.lower())
    return hash_object.hexdigest()

def is_seen(hash):
    """ Checks if hash is already in the table """
    
    return ds.search_hash(hash)


