from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from skilllens.config import DATABASE_URL
from skilllens.models import Base

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def create_tables() -> None:
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """
    Drop all database tables.
    Useful during early development.
    """
    Base.metadata.drop_all(bind=engine)


def get_db_session():
    """
    Create a database session.
    """
    with SessionLocal() as session:
        yield session