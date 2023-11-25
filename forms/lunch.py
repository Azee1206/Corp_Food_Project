from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LunchForm(FlaskForm):
    """Форма формирования"""

    submit_save = SubmitField('Оплатить по привязанной карте')
