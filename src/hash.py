import hashlib
import data_store as ds

def get_hash(job_description):
    """
    get_hash: takes in a text and returns a hash key
    """
    job_description = job_description.encode('utf-8')
    hash_object = hashlib.md5(job_description.lower())
    return hash_object.hexdigest()

def is_in_accepted(hash):
    """
    is_in_accepted: takes in a hash (str) and checks if the hash already exists in the acceptedJobs table
    """
    return ds.search_hash(hash, 'acceptedJobs')
    
def is_in_notaccepted(hash):
    """
    is_in_notaccepted: takes in a hash (str) and checks if the hash already exists in the notacceptedJobs table
    """
    return ds.search_hash(hash, 'notacceptedJobs')


