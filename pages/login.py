from __main__ import app, login_manager
from flask import render_template, redirect
from flask_login import login_user
from forms.user import LoginForm
from data import db_session
from data.user import User


@login_manager.user_loader
def load_user(user_id):
    """Загрузка зарегистрированного пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/login", methods=['GET', 'POST'])
async def login_page():
    """Обработка авторизации"""
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template(
        'login.html',
        form=form,
    )
