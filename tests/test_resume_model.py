import pytest
from bojojo.repositories import Resume

@pytest.mark.usefixtures("sqlite_db", "session", "valid_jobtitle_id")
class TestJobTitle:

    def test_create_resume(self, session, valid_jobtitle_id):
        
        session.execute(
            "INSERT INTO Resumes (job_title_id, file_path) VALUES(?, ?)",
            (valid_jobtitle_id, "/path/to/resume.pdf")
        )
        session.connection.comit()
        session.execute("SELECT * FROM Resumes WHERE file_path='/path/to/resume.pdf'")
        resume = session.fetchone()
        
        assert resume is not None
        assert resume[1] == valid_jobtitle_id
        assert resume[2] == "/path/to/resume.pdf"