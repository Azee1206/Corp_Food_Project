from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    """Форма голосования"""
    message = StringField('Сообщение', validators=[DataRequired()], render_kw={"placeholder": "Сообщение"})
    wishes = StringField('Пожелания', validators=[DataRequired()], render_kw={"placeholder": "Пожелания для бизнес-ланча"})
    submit = SubmitField('Отправить')
