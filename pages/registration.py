from __main__ import app
from flask import render_template, redirect
from forms.user import RegisterForm
from data import db_session
from data.user import User


@app.route("/registration", methods=['GET', 'POST'])
async def registration_page():
    """Обработка регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if len(form.password.data) < 5:
            return render_template(
                'registration.html',
                form=form,
                message="Слишком короткий пароль! Сделайте пароль от 5 символов"
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.fullname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template(
        'registration.html',
        form=form,
    )
