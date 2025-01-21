from sqlalchemy import Column, Integer, String
from database import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)