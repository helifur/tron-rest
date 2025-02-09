import sqlalchemy as sa
import sqlalchemy.orm as orm

import os
from dotenv import load_dotenv

__factory = None
load_dotenv()


def global_init() -> None:
    """Initialize a database"""
    global __factory

    if __factory:
        return

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")

    engine = sa.create_engine(f"postgresql://{user}:{password}@db:5432/{db_name}")
    __factory = orm.sessionmaker(bind=engine)

    from ..models import __all_models

    __all_models.transactions.Base.metadata.create_all(bind=engine)


def create_session() -> orm.Session:
    """Create a session"""
    global __factory
    return __factory()
