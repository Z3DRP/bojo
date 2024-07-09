import sqlite3
from sqlite3 import Error
from bojojo import DB_CREATE_ERROR

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        raise e
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        return e
    
def create_tables(connection):
    CREATE_APPLIED = """
    CREATE TABLE IF NOT EXISTS Applied_Jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        jobTitle TEXT NOT NULL,
        location TEXT NOT NULL,
        pay TEXT,
        apply_date TEXT NOT NULL
    );
    """

    CREATE_FAILED_APPLIED = """

    """

    CREATE_JOB_SPECIFICATIONS = """
    """

    CREATE_COMPLETED_RUNS = """
    CREATE TABLE IF NOT EXISTS Completed_Runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT NOT NULL,
        total_applicant_attempts INTEGER NOT NULL,
        successful_attempts INTEGER NOT NULL DEFAULT 0,
        failed_attempts INTEGER NOT NULL DEFAULT 0,
        date_ran TEXT NOT NULL,
        durration TEXT NOT NULL,
    )
    """
