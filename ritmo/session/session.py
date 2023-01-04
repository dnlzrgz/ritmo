from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ritmo.models import models


def create_session(path: str) -> sessionmaker:
    """
    Create a new session for the database.
    """

    Session = sessionmaker()
    engine = create_engine(path)

    models.Base.metadata.create_all(engine)

    Session.configure(bind=engine)

    return Session
