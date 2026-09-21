"""PostgreSQL connection and table bootstrap for the application."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database() -> None:
    # Import registers the mapped models before SQLAlchemy creates their tables.
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
