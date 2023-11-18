from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PaymentForm(FlaskForm):
    """Форма оплаты"""
    number = StringField('Номер карты', validators=[DataRequired()], render_kw={"placeholder": "Номер карты"})
    term = StringField('MM/ГГ', validators=[DataRequired()], render_kw={"placeholder": "MM/ГГ"})
    cvc = StringField('CVC', validators=[DataRequired()], render_kw={"placeholder": "CVC"})
    submit = SubmitField('Оплатить')
    save = SubmitField('Привязать')
    submit_save = SubmitField('Оплатить по привязанной карте')
