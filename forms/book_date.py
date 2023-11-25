from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import DateField, BooleanField, SelectField, SubmitField, RadioField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    """Форма бронирования стола"""
    date = DateField('Дата', validators=[DataRequired()], default=datetime.now())
    time = SelectField('Время', validators=[DataRequired()], choices=[])
    place1 = BooleanField('1')
    place2 = BooleanField('2')
    place3 = BooleanField('3')
    place4 = BooleanField('4')
    place5 = BooleanField('5')
    place6 = BooleanField('6')
    place7 = BooleanField('7')
    place8 = BooleanField('8')
    place9 = BooleanField('9')
    place10 = BooleanField('10')
    place11 = BooleanField('11')
    place12 = BooleanField('12')
    delivery = RadioField(choices=[("False", 'В столовой'), ("True", 'Доставка до рабочего места')])
    submit_payment = SubmitField("Оплатить")
    submit_payment_if_info = SubmitField("Оплатить по привязанной карте")

    def __getitem__(self, k):
        if k == '1':
            return self.place1
        if k == '2':
            return self.place2
        if k == '3':
            return self.place3
        if k == '4':
            return self.place4
        if k == '5':
            return self.place5
        if k == '6':
            return self.place6
        if k == '7':
            return self.place7
        if k == '8':
            return self.place8
        if k == '9':
            return self.place9
        if k == 'a':
            return self.place10
        if k == 'b':
            return self.place11
        if k == 'c':
            return self.place12