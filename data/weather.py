# описание структуры таблицы через SQLAlchemy как класса с определением полей и их типов

import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Weather(SqlAlchemyBase):
    # имя таблицы в БД
    __tablename__ = 'weather'
    # структура полей БД
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    humidity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pressure = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    temp_max = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    temp_min = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    clouds = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    wind_napr = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    wind_speed = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
