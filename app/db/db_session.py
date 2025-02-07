import sqlalchemy as sa
import sqlalchemy.orm as orm

__factory = None


def global_init() -> None:
    global __factory

    if __factory:
        return

    engine = sa.create_engine("postgresql://postgres:changeme@localhost:17936/postgres")
    __factory = orm.sessionmaker(bind=engine)

    from ..models import __all_models

    __all_models.transactions.Base.metadata.create_all(bind=engine)


def create_session() -> orm.Session:
    global __factory
    return __factory()
