import os
from flask import Flask, render_template, redirect
from flask import make_response, jsonify
from flask_login import LoginManager, login_required, logout_user
from forms.add import AddForm
from data import db_session
import api_food
from transliterate import translit
import schedule
import time
from table_check import check_tables
import threading
import asyncio

import aiohttp

from flask_restful import Api
from resources_api.user_resources import UserHistoryResource, UserCartResource, UserPaymentResource, UserNameSurResource
from resources_api.food_resources import FoodAllRecourse, FoodRecourse, FoodRatingRecourse
from resources_api.order_resources import OrderResource, OrderAllRecourse
from resources_api.table_resources import AllTableResources, TableResource


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
schedule.every().hour.at(":15").do(check_tables)
schedule.every().hour.at(":30").do(check_tables)
schedule.every().hour.at(":45").do(check_tables)
schedule.every().hour.at(":00").do(check_tables)

from pages import (default, registration, login, menu, basket, book,
                   payment, profile, orders)

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

api.add_resource(AllTableResources, "/api/all_tables")
api.add_resource(TableResource, "/api/table/<path:table_places_date_time>")

app.config['SECRET_KEY'] = "secret_key"


@app.errorhandler(404)
async def not_found(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
async def bad_request(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


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


@app.route('/lunch')
async def lunch_page():
    return render_template("lunch.html")


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


async def main():
    """Запуск сайта"""

    db_session.global_init("db/corp_food_info.db")
    app.register_blueprint(api_food.blueprint)
    check_tables()
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=run_schedule, daemon=True).start()
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
