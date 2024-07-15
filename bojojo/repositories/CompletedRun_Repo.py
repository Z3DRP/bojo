from sqlalchemy.orm import Session
from bojojo.repositories import repository


class CompletedRunRepository(repository):
    def __init__(self, session: Session):
        self.session = session    