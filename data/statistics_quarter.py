import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class StatisticsQuarter(SqlAlchemyBase, SerializerMixin):
    __tablename__ = ('statistics_per_month')
    text_id = sqlalchemy.Column(sqlalchemy.String, index=True, primary_key=True)
    food_name = sqlalchemy.Column(sqlalchemy.String)
    first_quarter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    second_quarter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    third_quarter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    fourth_quarter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
