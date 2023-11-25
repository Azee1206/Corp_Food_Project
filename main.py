import os
from flask import Flask, render_template, redirect
from flask import make_response, jsonify
from flask_login import LoginManager, login_required, logout_user
from forms.add import AddForm, DeleteForm
from data import db_session
import api_food
import schedule
import time
from table_check import check_tables
import threading
import asyncio

from flask_restful import Api
from resources_api.user_resources import UserHistoryResource, UserCartResource, UserPaymentResource, UserNameSurResource
from resources_api.food_resources import FoodAllRecourse, FoodRecourse, FoodRatingRecourse
from resources_api.order_resources import OrderResource, OrderAllRecourse
from resources_api.table_resources import AllTableResources, TableResource
from resources_api.statistics_resorces import AllStatisticsResources, StatisticResources, StatisticsQuarterResources


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
schedule.every().hour.at(":15").do(check_tables)
schedule.every().hour.at(":30").do(check_tables)
schedule.every().hour.at(":45").do(check_tables)
schedule.every().hour.at(":00").do(check_tables)

from pages import (default, registration, login, menu, basket, book,
                   payment, profile, orders, statistics, add_page)

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

api.add_resource(AllStatisticsResources, "/api/all_stat")
api.add_resource(StatisticResources, "/api/stat")
api.add_resource(StatisticsQuarterResources, "/api/month_stat")

app.config['SECRET_KEY'] = "secret_key"


@app.errorhandler(404)
async def not_found(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
async def bad_request(error):
    """Сообщение об ошибке, не найдена страница"""
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/logout')
@login_required
async def logout():

    """Выход из профиля"""

    logout_user()

    return redirect("/")


@app.route('/lunch')
async def lunch_page():
    return render_template("lunch.html")


@app.route('/delete')
async def delete_page():
    form2 = DeleteForm()
    return render_template("delete.html", form2=form2)


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
