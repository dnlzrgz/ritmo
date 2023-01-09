from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ritmo.models import Base


def create_session(path: str) -> sessionmaker:
    """
    Create a new session for the database at the given path.

    Args:
        path: The path to the database. It must be a valid SQLAlchemy connection string.
    """

    session = sessionmaker()
    engine = create_engine(path)

    Base.metadata.create_all(engine)

    session.configure(bind=engine)

    return session


def create_memory_session() -> sessionmaker:
    """
    Create a new session for an in-memory database.
    """

    return create_session("sqlite://")


def create_local_session() -> sessionmaker:
    """
    Create a new session for a local database at ~/.ritmo/ritmo.db.
    """

    home_dir = Path.home()

    config_folder = home_dir / ".ritmo"
    config_folder.mkdir(exist_ok=True)

    db_path = config_folder / "ritmo.db"

    return create_session(f"sqlite:///{db_path}")
