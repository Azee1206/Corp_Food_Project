from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    """Форма регистрации пользователя"""
    name = StringField('Имя', validators=[DataRequired()], render_kw={"placeholder": "Имя"})
    fullname = StringField('Фамилия', validators=[DataRequired()], render_kw={"placeholder": "Фамилия"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "E-mail"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()], render_kw={"placeholder": "Повторите пароль"})
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """Форма входа пользователя"""
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "E-mail"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    submit = SubmitField('Войти')
