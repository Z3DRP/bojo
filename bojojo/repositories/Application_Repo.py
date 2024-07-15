from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from bojojo.models import Application
from bojojo.repositories import repository


class ApplicationRepository(repository):

    def __init__(self, session: Session):
        self.session = session


    def get(self, id: int):
        try:
            result = self.session.execute(select(Application).where(Application.id==id)).scalars().first()
            return result
        except SQLAlchemyError as e:
            raise e