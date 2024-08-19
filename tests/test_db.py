import pytest
from sqlalchemy.exc import IntegrityError
import os
from bojo.repositories import db_init


@pytest.mark.db
@pytest.mark.usefixtures("sqlite_db", "session")
class DatabaseTest:

    def test_tables_created(self, session):
        session.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = session.fetchall()
        expected_tables = {
            "Job_Titles", "Resumes", "Job_Boards", "Scheduled_Runs",
            "Completed_Runs", "Applications"
        }
        created_tables = {table[0] for table in tables}
        assert created_tables == expected_tables


    def test_db_intialization(self, sqlite_db):
        assert sqlite_db is not None
        cursor = sqlite_db.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result is not None
