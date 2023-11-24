import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Statistics(SqlAlchemyBase, SerializerMixin):
    __tablename__ = ('statistics')
    text_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    food_name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    num_of_sales = sqlalchemy.Column(sqlalchemy.Integer)
    day = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.Integer)
