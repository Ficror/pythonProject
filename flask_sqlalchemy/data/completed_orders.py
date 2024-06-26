import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Completed_orders(SqlAlchemyBase):
    __tablename__ = "completed_orders"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    list_of_product = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relationship("User")
