import sqlite3
from sqlite3 import Error
import pandas as pd

def create_connection(db_file='visited_jobs.db'):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print('Table created')
    except Error as e:
        print(e)


def create_db():
    sql_create_acceptedJobs_table = """ CREATE TABLE IF NOT EXISTS acceptedJobs (
                                        hash text PRIMARY KEY,
                                        date_posted text,
                                        title text,
                                        company text,
                                        location text,
                                        level text,
                                        description text

                                    ); """
    sql_create_notacceptedJobs_table = """ CREATE TABLE IF NOT EXISTS notacceptedJobs (
                                        hash text PRIMARY KEY,
                                        date_posted text
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
    conn = create_connection('visited_jobs.db')
    sql = ''' INSERT INTO acceptedJobs(hash, date_posted, title, company, location, level, description)
              VALUES(?,?,?,?,?,?,?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, job)
        conn.commit()
        return cur.lastrowid

def insert_notaccepted_job(job):
    conn = create_connection('visited_jobs.db')
    sql = ''' INSERT INTO projects(hash, date_posted)
              VALUES(?,?) '''
    with conn:
        cur = conn.cursor()
        cur.execute(sql, job)
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


if __name__ == '__main__':
    # create_db()
    print_table('acceptedJobs')
    # to_csv('acceptedJobs')
    # insert_accepted_job(('123aaa4bbb', '01-01-2001', 'software engineer', 'amazon', 'San Francisco,CA', 'joonior', 'bla-bla-bla'))