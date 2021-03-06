import sqlite3
from sqlite3 import Error
import pandas as pd
from job_posting_class import Job_Posting
import os
import datetime
DATA_PATH = '/data'
CSV_PATH = '/data/csv'

def create_connection():
    """ Create and return a connection to db_file SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(os.path.join(DATA_PATH,"visited_jobs.db"))
        return conn
    except Error as e:
        print(e)

    return conn

def create_db():
    sql_create_table = """ 
                                        CREATE TABLE IF NOT EXISTS SeenJobs (
                                        hash text PRIMARY KEY,
                                        date_posted text,
                                        title text,
                                        company text,
                                        location text,
                                        level text,
                                        description text,
                                        link text,
                                        accepted int
                                    ); """
    
    conn = create_connection()
    with conn:
        try: 
            cur = conn.cursor()
            cur.execute(sql_create_table)
            conn.commit()
            print('Table created')
        except Error as e:
            print(f"Error while creating a table Error:\n{e}")

def drop_table():
    conn = create_connection()
    with conn:
        sql1 = """ DROP TABLE IF EXISTS SeenJobs """
        cur = conn.cursor()
        cur.execute(sql1)
        conn.commit()
    print('Dropped the table')

def insert_job(job):
    """ Insert a job object as columns into the table """

    job_tuple = (job.hash, job.date_posted, job.title, job.company, job.location, job.level, job.description, job.link, int(job.accepted))
    conn = create_connection()

    sql = ''' INSERT or IGNORE INTO SeenJobs(hash, date_posted, title, company, location, level, description, link, accepted)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, job_tuple)
        conn.commit()
        # print('Inserted job')
        return cur.lastrowid

def print_table(table):
    conn = create_connection()
    cur = conn.execute('select * from ' + table)
    # To print columns only
    # cols = list(map(lambda x: x[0], cur.description))
    # print(cols)
    #  to print all contents of a table
    print(cur.fetchall())

def to_csv(accepted=True):
    """ Output jobs (accepted by default) into a CSV file called acceptedJobs.csv """

    sql_query = 'SELECT * FROM SeenJobs WHERE accepted=1' if accepted else 'SELECT * FROM SeenJobs WHERE accepted=0'
    file_name = 'accepted_jobs' if accepted else 'not_accepted_jobs'

    conn = create_connection()
    with conn:
        table = pd.read_sql_query(sql_query, conn)
        if not os.path.exists(CSV_PATH):
            os.mkdir(CSV_PATH)
        file = os.path.join(CSV_PATH, file_name + datetime.datetime.now().strftime("_%Y-%m-%d_%H:%M") + '.csv')
        table.to_csv(file, index_label='index')

        print('Exported table to CSV')

def cache_hashes():
    conn = create_connection()
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

def search_hash(hash):
    """ checks if hash exists in the table
        returns True if found, False if not found
    """
    conn = create_connection()
    with conn:
        cur = conn.execute('SELECT * FROM SeenJobs WHERE hash=?',(hash,))
        return len(cur.fetchall()) > 0


if __name__ == '__main__':
    # drop_table()
    # create_db()

    # job1 = Job_Posting('12345', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'junior', 'long description', 'httplink', True)
    # job2 = Job_Posting('64737227', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'associate', 'long description', 'httplink', False)
    # insert_job(job1)
    # insert_job(job2)
    to_csv()

    # assert search_hash('12345') == True, "Job 12345 does not exist"
    # assert search_hash('64737227') == True, "Job 64737227 does not exist"

