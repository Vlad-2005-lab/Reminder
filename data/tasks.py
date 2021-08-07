import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tasks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.Integer)
    last_time = sqlalchemy.Column(sqlalchemy.String)
