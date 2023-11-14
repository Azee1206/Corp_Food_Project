from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    """Форма оплаты"""
    number = StringField('Номер карты', validators=[DataRequired()])
    term = StringField('MM/ГГ', validators=[DataRequired()])
    cvc = StringField('CVC', validators=[DataRequired()])
    submit = SubmitField('Оплатить')
    save = SubmitField('Привязать')
