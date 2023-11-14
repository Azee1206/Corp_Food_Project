import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Food(SqlAlchemyBase, SerializerMixin):
    """Форма создания таблицы блюд"""
    __tablename__ = 'orders'
    order_number = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    order_info = sqlalchemy.Column(sqlalchemy.String)  # информация о блюдах, которые входят в заказ
    client_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
