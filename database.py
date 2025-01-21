import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import os

SqlAlchemyBase = declarative_base()  # Базовый класс для всех моделей
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("site.db")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from models import user  # Здесь нужно импортировать все модели

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if __factory is None:
        raise Exception("База данных не инициализирована. Вызовите global_init() перед использованием.")
    return __factory()