import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    order_number = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    order_info = sqlalchemy.Column(sqlalchemy.String)  # информация о блюдах, которые входят в заказ
    client_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    name_sur = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_done = sqlalchemy.Column(sqlalchemy.Boolean, default=0)
