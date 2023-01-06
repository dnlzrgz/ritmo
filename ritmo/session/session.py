from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ritmo.models import models


def create_session(path: str) -> sessionmaker:
    """
    Create a new session for the database at the given path.

    Args:
        path: The path to the database. It must be a valid SQLAlchemy connection string.
    """

    Session = sessionmaker()
    engine = create_engine(path)

    models.Base.metadata.create_all(engine)

    Session.configure(bind=engine)

    return Session


def create_memory_session() -> sessionmaker:
    """
    Create a new session for an in-memory database.
    """

    return create_session("sqlite://:memory:")


def create_local_session() -> sessionmaker:
    """
    Create a new session for a local database at ~/.ritmo/ritmo.db.
    """

    home_dir = Path.home()

    config_folder = home_dir / ".ritmo"
    config_folder.mkdir(exist_ok=True)

    db_path = config_folder / "ritmo.db"

    return create_session(f"sqlite:///{db_path}")
