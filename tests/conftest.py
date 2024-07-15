from unittest.mock import MagicMock
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from bojojo.models.Application import Base
from bojojo.repositories import db_init
from bojojo.repositories.Resume_Repo import ResumeRepository
from bojojo.models import Job_Title, Resume
from bojojo.services.resume_service import ResumeService


# used for testing db file initialization
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


# used for testing db file initialization
@pytest.fixture(scope="module")
def session(sqlite_db):
    """Provide a transactional scope"""
    conn = sqlite_db
    cursor = conn.cursor()
    yield cursor
    conn.rollback()


@pytest.fixture(scope="module")
def db_session(sqlite_db):
    temp_db_path = sqlite_db
    engine = create_engine(f'sqlite:///{temp_db_path}')
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def simulated_db_err():
    return "Simulated DB error"


@pytest.fixture(scope="module")
def valid_jobtitle_id(session):
    session.execute(
        "INSERT INTO Job_Titles (name, experience_level, experience_years) VALUES(?, ?, ?)",
        ("Software Developer", "mid", 3)
    )
    job_title_id = session.lastrowid
    session.connection.comit()
    return job_title_id


@pytest.fixture(scope="module")
def jobtitle_id(db_session):
    db_session.execute(
        "INSERT INTO Job_Titles (name, experience_level, experience_years) VALUES(?, ?, ?)",
        ("Database Developer", "mid", 3)
    )
    jtid = db_session.lastrowid
    db_session.connection.comit()
    return jtid


@pytest.fixture(scope="module")
def mock_resume_repo():
    return MagicMock(spec=ResumeRepository)


@pytest.fixture(scope="module")
def resume_repo(session: Session):
    return ResumeRepository(session)


@pytest.fixture(scope="module")
def mock_resume_service(mock_resume_repo):
    return ResumeService(mock_resume_repo)


@pytest.fixture(scope="module")
def resume_path():
    return '/usr/docs/rsm.pdf'


@pytest.fixture(scope="module")
def a_resume(db_session: Session, jobtitle_id: int):
    db_session.execute(
        "INSERT INTO Resumes (name, job_title_id, file_path) VALUES(?, ?, ?)",
        ("Db admin", jobtitle_id, 'resume/path')
    )
    return db_session.get(Resume, {"name": "Db admin"})

