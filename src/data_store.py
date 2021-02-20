import sqlite3
from sqlite3 import Error
import pandas as pd
from job_posting_class import Job_Posting

def create_connection(db_file='visited_jobs.db'):
    """ Create and return a connection to db_file SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement

    Keywork arguments:
    conn -- connection object
    create_table_sql -- a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print('Table created')
    except Error as e:
        print(e)


def create_db():
    sql_create_acceptedJobs_table = """ 
                                        CREATE TABLE IF NOT EXISTS acceptedJobs (
                                        hash text PRIMARY KEY,
                                        date_posted text,
                                        title text,
                                        company text,
                                        location text,
                                        level text,
                                        description text,
                                        link text

                                    ); """
    sql_create_notacceptedJobs_table = """  
                                        CREATE TABLE IF NOT EXISTS notacceptedJobs (
                                        hash text PRIMARY KEY,
                                        date_posted text,
                                        title text,
                                        company text,
                                        location text,
                                        level text,
                                        description text,
                                        link text
                                        ); """
    
    conn = create_connection('visited_jobs.db')
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_acceptedJobs_table)

        # create tasks table
        create_table(conn, sql_create_notacceptedJobs_table)
    else:
        print("Error! cannot create the database connection.")


def insert_accepted_job(job):
    """Insert a job object as columns into the accepted table"""

    job_tuple = (job.hash, job.date_posted, job.title, job.company, job.location, job.level, job.description, job.link)
    conn = create_connection('visited_jobs.db')
    sql = ''' INSERT or IGNORE INTO acceptedJobs(hash, date_posted, title, company, location, level, description, link)
              VALUES(?,?,?,?,?,?,?,?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, job_tuple)
        conn.commit()
        return cur.lastrowid

def insert_notaccepted_job(job):
    """Insert a job into the notaccepted table"""
    job_tuple = (job.hash, job.date_posted, job.title, job.company, job.location, job.level, job.description, job.link)
    conn = create_connection('visited_jobs.db')
    sql = ''' INSERT or IGNORE INTO notacceptedJobs(hash, date_posted, title, company, location, level, description, link)
              VALUES(?,?,?,?,?,?,?,?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, job_tuple)
        conn.commit()
        return cur.lastrowid

def print_table(table):
    conn = create_connection('visited_jobs.db')
    cur = conn.execute('select * from ' + table)
    # to print columns only
    # cols = list(map(lambda x: x[0], cur.description))
    # print(cols)
    #  to print all contents of a table
    print(cur.fetchall())

def to_csv(table_name):
    with sqlite3.connect('visited_jobs.db') as db:
        table = pd.read_sql_query('SELECT * from ' + table_name, db)
        table.to_csv(table_name + '.csv', index_label='index')

def drop_tables():
    conn = create_connection('visited_jobs.db')
    with conn:
        sql1 = '''DROP TABLE IF EXISTS acceptedJobs'''
        sql2 = '''DROP TABLE IF EXISTS notacceptedJobs'''
        cur = conn.cursor()
        cur.execute(sql1)
        cur.execute(sql2)
        conn.commit()
    print('Dropped tables')

def cache_hashes():
    conn = create_connection('visited_jobs.db')
    accepted_jobs = {}
    not_accepted_jobs = {}
    with conn:
        cur1 = conn.execute('SELECT hash FROM acceptedJobs')
        accepted_jobs = cur1.fetchall()
        cur1 = conn.execute('SELECT hash FROM notacceptedJobs')
        not_accepted_jobs = cur1.fetchall()
    print('Cached hashes from both tables')
    for j in range(len(accepted_jobs)):
        accepted_jobs[j] = accepted_jobs[j][0]
    for j in range(len(not_accepted_jobs)):
        not_accepted_jobs[j] = not_accepted_jobs[j][0]

    return set(accepted_jobs), set(not_accepted_jobs)

def search_hash(hash, table):
    """ checks if hash exists in the table
        returns True if found, False if not found
    """
    conn = create_connection('visited_jobs.db')
    with conn:
        cur = conn.execute('SELECT * FROM ' + table + ' WHERE hash=?',(hash,))
        return len(cur.fetchall()) > 0


if __name__ == '__main__':
    # drop_tables()
    # create_db()
    # print_table('acceptedJobs')
    # to_csv('acceptedJobs')
    # insert_accepted_job(('123aaa4bbb', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'joonior', 'bla-bla-bla', 'httplink'))
    # insert_notaccepted_job(('hashbrown123', '01-01-2001'))

    # print_table('notacceptedJobs')
    # accepted, not_accepted = cache_hashes()
    # print('Accepted: ', accepted)
    # print('Not Accepted: ', not_accepted)
    # job1 = Job_Posting('111aaa4bbb', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'joonior', 'bla-bla-bla', 'httplink')
    # job2 = Job_Posting('hashbrown00', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'joonior', 'bla-bla-bla', 'httplink')
    # insert_accepted_job(job1)
    # insert_notaccepted_job(job2)

    assert search_hash('111aaa4bbb', 'acceptedJobs') == True, "Job 111aaa4bbb does not exist"
    assert search_hash('hashbrown00', 'notacceptedJobs') == True, "Job hashbrown00 does not exist"

