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
    
def initialize_db(path):
    try:
        create_tables(path)
        create_indexes(path)
    except Error as e:
        raise e
    

def create_indexes(path:str) -> None:
    connection = create_connection(path)
    indexes = [
        "CREATE INDEX IF NOT EXISTS appname_idx ON Applications (name)",
        "CREATE INDEX IF NOT EXISTS app_jobtitle_idx ON Applications (job_title_id)",
        "CREATE INDEX IF NOT EXISTS app_jobboard_idx ON Applications (job_board_id)",
        "CREATE INDEX IF NOT EXISTS app_company_idx ON Applications (company)",
        "CREATE INDEX IF NOT EXISTS jobtitle_name_idx ON Job_Titles (name)",
        "CREATE INDEX IF NOT EXISTS resume_name_idx ON Resumes (name)",
        "CREATE INDEX IF NOT EXISTS resume_jobtitle_idx ON Resumes (job_title_id)",
        "CREATE INDEX IF NOT EXISTS jobboard_name_idx ON Job_Boards (name)",
        "CREATE INDEX IF NOT EXISTS jobboard_easy_idx ON Job_Boards(has_easy_apply)",
        "CREATE INDEX IF NOT EXISTS schedrun_jobtitle_idx ON Scheduled_Runs (job_title_id)",
        "CREATE INDEX IF NOT EXISTS schedrun_job_board_idx ON Scheduled_Runs (job_board_id)",
        "CREATE INDEX IF NOT EXISTS schedrun_runday_idx ON Scheduled_Runs (run_dayof_week)",
        "CREATE INDEX IF NOT EXISTS comprun_executiondate_idx ON Completed_Runs (execution_date)",
        "CREATE INDEX IF NOT EXISTS comprun_applicationsubmit_idx ON Completed_Runs (applications_submitted)",
        "CREATE INDEX IF NOT EXISTS comprun_failedsubmits_idx ON Completed_Runs (failed_submissions)",
        "CREATE INDEX IF NOT EXISTS comprun_runid_idx ON Completed_Runs (run_id)"
    ]

    for index_stmnt in indexes:
        connection.execute(index_stmnt)
    connection.commit()
    connection.close()


def create_tables(path:str) -> None:
        connection = create_connection(path)

        CREATE_JOB_TITLES = """
        CREATE TABLE IF NOT EXISTS Job_Titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            experience_level TEXT NOT NULL CHECK (experience_level IN ('junior', 'mid', 'senior')),
            experience_years REAL NOT NULL DEFAULT 0
        );
        """

        CREATE_RESUMES = """
        CREATE TABLE IF NOT EXISTS Resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            job_title_id INTEGER,
            file_path TEXT NOT NULL,
            FOREIGN KEY (job_title_id)
                REFERENCES Job_Titles (id)
        );
        """

        CREATE_JOB_BOARDS = """
        CREATE TABLE IF NOT EXISTS Job_Boards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            has_easy_apply INTEGER NOT NULL DEFAULT 0 CHECK (has_easy_apply IN (0, 1))
        );
        """

        CREATE_SCHEDULED_RUNS = """
        CREATE TABLE IF NOT EXISTS Scheduled_Runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            creation_date TEXT NOT NULL,
            job_title_id INTEGER NOT NULL,
            job_board_id INTEGER NOT NULL,
            run_dayOf_week TEXT,
            run_day INTEGER,
            run_time TEXT,
            run_month TEXT,
            run_type TEXT CHECK (run_type IN ('once', 'reboot', 'daily', 'hourly', 'weekly', 'monthly', 'midnight')),
            recurring INTEGER DEFAULT 0 CHECK (recurring IN (0, 1)),
            easy_apply_only INTEGER NOT NULL DEFAULT 0 CHECK (easy_apply_only IN (0, 1)),
            durration_minutes REAL,
            every_hour INTEGER,
            every_minute INTEGER,
            number_of_submissions INTEGER,
            FOREIGN KEY (job_title_id)
                REFERENCES Job_Titles (id),
            FOREIGN KEY (job_board_id)
                REFERENCES Job_Boards (id)
        );
        """

        CREATE_COMPLETED_RUNS = """
        CREATE TABLE IF NOT EXISTS Completed_Runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_date TEXT NOT NULL,
            start TEXT NOT NULL,
            finish TEXT NOT NULL,
            applications_submitted INTEGER NOT NULL DEFAULT 0,
            failed_submissions INTEGER NOT NULL DEFAULT 0,
            run_id INTEGER NOT NULL,
            FOREIGN KEY (run_id)
                REFERENCES Scheduled_Runs (id)
        );
        """

        CREATE_APPLICATIONS = """
        CREATE TABLE IF NOT EXISTS Applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            job_title_id INTEGER NOT NULL,
            job_board_id INTEGER NOT NULL,
            location TEXT NOT NULL,
            pay REAL,
            apply_date TEXT NOT NULL,
            submitted_successfully INTEGER NOT NULL DEFAULT 0 CHECK (submitted_successfully IN (0, 1)),
            run_id INTEGER,
            FOREIGN KEY (run_id)
                REFERENCES Completed_Runs (id)
            FOREIGN KEY (job_title_id)
                REFERENCES Job_Titles (id)
            FOREIGN KEY (job_board_id)
                REFERENCES Job_Boards (id)
        );
        """

        execute_query(connection, CREATE_JOB_TITLES)
        execute_query(connection, CREATE_RESUMES)
        execute_query(connection, CREATE_JOB_BOARDS)
        execute_query(connection, CREATE_SCHEDULED_RUNS)
        execute_query(connection, CREATE_COMPLETED_RUNS)
        execute_query(connection, CREATE_APPLICATIONS)


