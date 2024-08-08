
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def init_db_models(engine):
    Base.metadata.create_all(bind=engine)