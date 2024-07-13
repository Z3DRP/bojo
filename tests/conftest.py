import pytest
import sqlite3
import tempfile
import os
from bojojo.repositories import db_init
from bojojo.models import Job_Title

@pytest.fixture(scope="module")
def sqlite_db():
    temp_db_file = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
    temp_db_path = temp_db_file.name
    temp_db_file.close()
    db_init.initialize_db(temp_db_path)
    conn = db_init.create_connection(temp_db_path)
    yield conn
    conn.close()
    os.unlink(temp_db_path)

@pytest.fixture(scope="module")
def session(sqlite_db):
    """Provide a transactional scope"""
    conn = sqlite_db
    cursor = conn.cursor()
    yield cursor
    conn.rollback()

@pytest.fixture(scope="module")
def valid_jobtitle_id(session):
    session.execute(
        "INSERT INTO Job_Titles (name, experience_level, experience_years) VALUES(?, ?, ?)",
        ("Software Developer", "mid", 3)
    )
    job_title_id = session.lastrowid
    session.connection.comit()
    return job_title_id