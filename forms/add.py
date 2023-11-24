from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    """Форма добавления блюда"""
    name = StringField('Название', validators=[DataRequired()], render_kw={"placeholder": "Название"})
    type = SelectField('Категория', choices=['Завтрак', 'Первое', 'Второе', 'Салат', 'Десерт', 'Напиток'], validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()], render_kw={"placeholder": "Описание"})
    composition = StringField('Состав', validators=[DataRequired()], render_kw={"placeholder": "Состав"})
    calories = StringField('Калорийность(в ккал)', validators=[DataRequired()], render_kw={"placeholder": "Калорийность(в ккал)"})
    proteins = StringField('Белки(в граммах)', validators=[DataRequired()], render_kw={"placeholder": "Белки(в граммах)"})
    fats = StringField('Жиры(в граммах)', validators=[DataRequired()], render_kw={"placeholder": "Жиры(в граммах)"})
    carb = StringField('Углеводы(в граммах)', validators=[DataRequired()], render_kw={"placeholder": "Углеводы(в граммах)"})
    price = StringField('Цена', validators=[DataRequired()], render_kw={"placeholder": "Цена"})
    image = FileField('Изображение', render_kw={"placeholder": "Изображение блюда"})
    submit = SubmitField('Добавить')


class DeleteForm(FlaskForm):
    """Форма удаления блюда"""
    name = SelectField('Блюдо', validators=[DataRequired()], choices=[])
    submit = SubmitField('Удалить')
