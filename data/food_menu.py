import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Food(SqlAlchemyBase, SerializerMixin):
    """Форма создания таблицы блюд"""
    __tablename__ = 'food_menu'
    name = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.String)  # Тип блюда (холодное, горячие и тд)
    composition = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    visible = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    calories_proteins = sqlalchemy.Column(sqlalchemy.String)    # Информация о калориях, белках, жирах и углеводах разделенный ";"
    rating = sqlalchemy.Column(sqlalchemy.Float)
    text_id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, unique=True, index=True)
