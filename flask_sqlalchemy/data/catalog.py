import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Catalog(SqlAlchemyBase):
    __tablename__ = "catalog"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, unique=True)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    size = sqlalchemy.Column(sqlalchemy.String)
    in_basket = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    in_favorite = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    type = sqlalchemy.Column(sqlalchemy.String)