import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class StatisticsMonth(SqlAlchemyBase, SerializerMixin):
    __tablename__ = ('statistics_per_month')
    text_id = sqlalchemy.Column(sqlalchemy.String, index=True)
    food_name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    january = sqlalchemy.Column(sqlalchemy.Integer)
    february = sqlalchemy.Column(sqlalchemy.Integer)
    march = sqlalchemy.Column(sqlalchemy.Integer)
    april = sqlalchemy.Column(sqlalchemy.Integer)
    may = sqlalchemy.Column(sqlalchemy.Integer)
    june = sqlalchemy.Column(sqlalchemy.Integer)
    july = sqlalchemy.Column(sqlalchemy.Integer)
    august = sqlalchemy.Column(sqlalchemy.Integer)
    september = sqlalchemy.Column(sqlalchemy.Integer)
    october = sqlalchemy.Column(sqlalchemy.Integer)
    november = sqlalchemy.Column(sqlalchemy.Integer)
    december = sqlalchemy.Column(sqlalchemy.Integer)