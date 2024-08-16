
from bojojo.base_repo.repository import Repository
from bojojo.providers.db_session_provider import session_provider


def create_repo(repo_type: type[Repository]):
    return repo_type(session_provider())
    
    