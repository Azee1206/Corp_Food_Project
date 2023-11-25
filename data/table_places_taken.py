import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class TakenPlace(SqlAlchemyBase, SerializerMixin):
    """Форма создания таблицы столов"""
    __tablename__ = 'places_taken'
    table_place_info = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)