import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Tables(SqlAlchemyBase, SerializerMixin):
    """Форма создания таблицы столов"""
    __tablename__ = 'tables'
    table_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    seats = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)  # Имеет вид {номер стола}_{пуст или нет}; 1_True;2_False;3_True и тд
