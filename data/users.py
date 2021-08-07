import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    list_of_tasks = sqlalchemy.Column(sqlalchemy.String, default="")
    time_zone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    night_writing = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
