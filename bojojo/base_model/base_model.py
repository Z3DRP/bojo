
from sqlalchemy.orm import DeclarativeBase

Base = DeclarativeBase()


def init_db_models(engine):
    Base.metadata.create_all(bind=engine)