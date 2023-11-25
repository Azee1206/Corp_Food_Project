import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Statistics(SqlAlchemyBase, SerializerMixin):
    __tablename__ = ('statistics')
    text_id = sqlalchemy.Column(sqlalchemy.String, index=True, primary_key=True)
    food_name = sqlalchemy.Column(sqlalchemy.String)
    num_of_sales = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    day = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.Integer)


