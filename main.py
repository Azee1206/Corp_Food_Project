import datetime
import os
from flask import Flask, render_template, redirect
from flask import make_response, jsonify
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from forms.user import RegisterForm, LoginForm
from forms.add import AddForm, DeleteForm
from forms.book_date import BookForm
from forms.payment import PaymentForm
from data import db_session
from data.user import User
import api_food
from requests import get
from transliterate import translit
from create_readable_history import create_readable_history
import asyncio
import aiohttp
from flask_restful import Api
from resources_api.user_resources import UserHistoryResource, UserCartResource, UserPaymentResource, UserNameSurResource
from resources_api.food_resources import FoodAllRecourse, FoodRecourse, FoodRatingRecourse
from resources_api.order_resources import OrderResource, OrderAllRecourse

app = Flask(__name__)
api = Api(app)

api.add_resource(UserHistoryResource, '/api/user/history/<int:user_id>')
api.add_resource(UserCartResource, '/api/user/cart/<int:user_id>')
api.add_resource(UserPaymentResource, '/api/user/payment/<int:user_id>')
api.add_resource(UserNameSurResource, "/api/user/name_sur/<int:user_id>")

api.add_resource(FoodAllRecourse, '/api/food_all/<path:visible_foodtype>')
api.add_resource(FoodRecourse, "/api/food/<food_id>")
api.add_resource(FoodRatingRecourse, "/api/food/rating")
api.add_resource(OrderAllRecourse, "/api/all_orders")
api.add_resource(OrderResource, "/api/orders/<order_id>")

app.config['SECRET_KEY'] = "secret_key"

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
async def not_found(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
async def bad_request(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    """Загрузка зарегистрированного пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
async def default_page():
    """Обработка главной страницы"""
    return render_template("main.html")


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


@app.route('/menu/rate/<path:info>')
async def rate_food(info):
    session = aiohttp.ClientSession()
    # первый элемент info - тип блюда, второй - оценка, третий - id оцениваемого блюда
    info = info.split("/")
    food_type = info[0]
    await session.post(f"http://localhost:5000/api/food/rating", json={"food_id": info[2], "rate": info[1]})
    await session.close()
    return redirect(f'/menu/{food_type}')


@app.route('/menu/<food_type>')
async def menu_page(food_type):
    """Обработка страницы меню"""

    session = aiohttp.ClientSession()

    food_list_response = await session.get(f'http://localhost:5000/api/food_all/1/{food_type}')
    food_list_json = await food_list_response.json()
    food_list = food_list_json["food"]
    await session.close()

    if current_user.is_authenticated:
        if current_user.role == 'admin':
            food_list.append('add')
    return render_template('menu.html', food_list=food_list, cur_usr=current_user)


@app.route("/pay_if_payment_info", methods=["GET", "POST"])
async def pay_if_payment_info():
    session = aiohttp.ClientSession()
    await session.post(f"http://localhost:5000/api/user/history/{current_user.id}")
    name_sur_info = await session.get(f"http://localhost:5000/api/user/name_sur/{current_user.id}")
    name_sur_json = await name_sur_info.json()
    name_sur = f"{name_sur_json['name']} {name_sur_json['sur']}"
    await session.post("http://localhost:5000/api/orders/none",
                       json={"order_info": current_user.cart,
                             "client_id": current_user.id,
                             "name_sur": name_sur})
    await session.close()

    msg = "Оплата проведена успешно"
    return render_template("basket.html", message=msg, food_list=[])


@app.route('/book', methods=['GET', 'POST'])
def book_page():
    """Обработка страницы бронирования"""
    form_book = BookForm()
    time_choices = []
    current_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=19)

    while current_time <= end_time:
        time_choices.append((current_time.strftime('%H:%M'), current_time.strftime('%H:%M')))
        current_time += datetime.timedelta(minutes=15)

    form_book.time.choices = time_choices
    msg = ""
    table_list = get('http://localhost:5000/api/table').json()['tables']
    table12_list = [i for i in table_list if len(i['seats'].split(';')) == 12]
    table6_list = [i for i in table_list if len(i['seats'].split(';')) == 6]
    return render_template('book.html', message=msg, form_book=form_book,
                           table12_list=table12_list, table6_list=table6_list, cur_usr=current_user)


@app.route('/food_delete/<path:inf>', methods=['GET', 'POST'])
@login_required
async def delete_food_from_cart(inf):
    """Удаления блюда из корзины"""

    session = aiohttp.ClientSession()
    usr_id, food_id, amount = inf.split("/")
    await session.post(f"http://localhost:5000/api/user/cart/{usr_id}",
                       json={"food_id": food_id, "amount": -int(amount)})
    await session.close()

    return redirect('/basket')


@app.route('/food_add/<path:inf>', methods=['GET', 'POST'])
@login_required
async def add_food_to_cart(inf):
    """Добавление блюда в корзину"""

    session = aiohttp.ClientSession()
    usr_id, food_id, food_type = inf.split("/")
    await session.post(f"http://localhost:5000/api/user/cart/{usr_id}",
                       json={"food_id": food_id, "amount": 1})
    await session.close()

    return redirect(f'/menu/{food_type}')


@app.route('/basket', methods=['GET', "POST"])
@login_required
async def basket_page():
    """Обработка корзины"""

    session = aiohttp.ClientSession()
    food_list_response = await session.get(f"http://localhost:5000/api/user/cart/{current_user.id}")
    food_list = await food_list_response.json()
    empty = False
    if len(food_list["cart"]) == 0:
        empty = True
    return render_template('basket.html', food_list=food_list, cur_usr=current_user, empty=empty)


@app.route('/add', methods=['GET', 'POST'])
@login_required
async def add_page():
    """Обработка добавления блюда в меню"""
    type_converse = {'Первое': 'first', 'Второе': 'second', 'Салат': 'salads', 'Напиток': 'drinks', "Десерт": "desserts"}
    form = AddForm()
    msg = ""

    try:
        if form.validate_on_submit():
            text_id = translit(form.name.data.split()[0], language_code='ru', reversed=True).lower()
            session = aiohttp.ClientSession()
            await session.post(f"http://localhost:5000/api/food/none",
                               json={"name": form.name.data, "type": type_converse[form.type.data],
                                     "composition": form.composition.data, "description": form.description.data,
                                     "price": form.price.data, "text_id": text_id, "calories": form.calories.data,
                                     "proteins": form.proteins.data, "fats": form.fats.data,
                                     "carbohydrates": form.carb.data})
            img = form.image.data
            img.save(os.path.join(app.root_path, "static", "img", f"{text_id}.png"))
            await session.close()

    except Exception as e:
        msg = "При создании блюда произошла ошибка"
        print(e)

    return render_template('add.html', form=form, message=msg)


@app.route('/logout')
@login_required
async def logout():
    """Выход из профиля"""

    logout_user()

    return redirect("/")


@app.route("/profile", methods=['GET', 'POST'])
async def profile_page():
    """Обработка страницы профиля"""

    form = PaymentForm()

    session = aiohttp.ClientSession()

    payment_inf_res = await session.get(f"http://localhost:5000/api/user/payment/{current_user.id}")
    payment_inf_json = await payment_inf_res.json()
    payment_inf = payment_inf_json["result"]
    payment_inf[0] = f"{payment_inf[0][:4]}{'*' * (len(payment_inf[0]) - 8)}{payment_inf[0][-4:]}"
    payment_inf[0] = str(payment_inf[0])
    payment_inf[2] = f"{payment_inf[2][0]}**"

    history_result = await session.get(f"http://localhost:5000/api/user/history/{current_user.id}")
    history_json = await history_result.json()
    history = history_json["history"]
    history_res = await create_readable_history(history)

    if form.validate_on_submit():
        number = form.number.data
        term = form.term.data
        cvc = form.cvc.data

        msg_res = await session.post(f"http://localhost:5000/api/user/payment/{current_user.id}",
                                     json={"number": number, "term": term, "cvc": cvc})

        msg_json = await msg_res.json()
        msg = msg_json["msg"]
        await session.close()

        return render_template("profile.html", payment_inf=payment_inf, form_payment=form, history=history_res, message=msg)

    await session.close()
    return render_template("profile.html", payment_inf=payment_inf, form_payment=form, history=history_res)


@app.route('/payment', methods=['GET', 'POST'])
async def payment_page():
    form_payment = PaymentForm()
    if form_payment.validate_on_submit():
        if (not form_payment.number.data.isdigit()) or (len(form_payment.number.data) not in {13, 15, 16, 18, 19}):
            msg = "Некорректный формат номера карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        term = form_payment.term.data
        if "/" not in term:
            msg = "Некорректный формат срока годности карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        term = term.split("/")
        if (not term[0].isdigit()) or (not term[1].isdigit()):
            msg = "Некорректный формат срока годности карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        if not form_payment.cvc.data.isdigit() or len(form_payment.cvc.data) != 3:
            msg = "Некорректный формат cvc кода"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        sessionn = aiohttp.ClientSession()
        await sessionn.post(f"http://localhost:5000/api/user/history/{current_user.id}")
        await sessionn.post("http://localhost:5000/api/orders/none",
                            json={"order_info": current_user.cart, "client_id": current_user.id})
        await sessionn.close()
        msg = "Оплата проведена успешно"
        return render_template("basket.html", message=msg, food_list=[])
    return render_template("payment.html", form_payment=form_payment)


@app.route('/lunch')
async def lunch_page():
    return render_template("lunch.html")


@app.route('/orders')
async def orders_page():
    session = aiohttp.ClientSession()
    orders = await session.get(f"http://localhost:5000/api/all_orders")
    orders_json = await orders.json()
    orders_json = orders_json["orders"]
    return render_template("orders.html", orders=orders_json)


@app.route('/statistics/<statistics_type>')
async def statistics_page(statistics_type):
    if statistics_type == 'month':
        return render_template("statistics_month.html")
    if statistics_type == 'day':
        return render_template("statistics_day.html")


@app.route('/delete')
async def delete_page():
    form2 = DeleteForm()
    return render_template("delete.html", form2=form2)


async def main():
    """Запуск сайта"""

    db_session.global_init("db/corp_food_info.db")
    app.register_blueprint(api_food.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
