import flask
from flask import jsonify
from data import db_session
from data.food_menu import Food
from data.user import User
from data.tabels import Tables
from flask import request


blueprint = flask.Blueprint(
    'food_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/food', methods=['GET'])
async def get_food():
    """Функция получения ВСЕХ блюд из базы данных"""
    db_sess = db_session.create_session()
    food = db_sess.query(Food).all()
    return jsonify(
        {
            "food":
                [item.to_dict(only=
                              ("name", "type", "composition", "description", "price", "visible", "text_id", "calories_proteins"))
                 for item in food]
        }
    )


@blueprint.route('/api/food/<food_id>', methods=['GET'])
async def get_one_food(food_id):
    """Функция получения ОДНОГО блюда из базы данных"""
    db_sess = db_session.create_session()
    food = db_sess.query(Food).get(food_id)
    if not food:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'food': food.to_dict(only=
                                 ("name", "type", "composition", "description", "price", "visible", "text_id", "calories_proteins"))
        }
    )


@blueprint.route('/api/food', methods=['POST'])
async def create_food():
    """Функция добавления в базу данных блюда"""
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["name", "type", "composition", "description", "price",
                  "text_id", "calories", "proteins", "fats", "carbohydrates"]):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    calories_info = (f'{request.json["calories"]} ккал;{request.json["proteins"]} г;'
                     f'{request.json["fats"]} г;{request.json["carbohydrates"]} г')
    food = Food(
        name=request.json["name"],
        type=request.json["type"],
        composition=request.json["composition"],
        description=request.json["description"],
        price=request.json["price"],
        text_id=request.json["text_id"],
        calories_proteins=calories_info,
        rating=5
    )
    db_sess.add(food)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/table', methods=["GET"])
async def get_all_tables():
    """Функция получения информации о ВСЕХ столах"""
    db_sess = db_session.create_session()
    tables = db_sess.query(Tables).all()
    return jsonify(
        {
            "tables":
                [item.to_dict(only=
                              ("table_id", "seats"))
                 for item in tables]
        }
    )


@blueprint.route('/api/food/<table_id>', methods=['GET'])
async def get_one_table(table_id):
    """Функция получения информации об ОДНОМ столе"""
    db_sess = db_session.create_session()
    table = db_sess.query(Tables).get(table_id)
    if not table:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'table': table.to_dict(only=
                                 ("table_id", "seats"))
        }
    )


@blueprint.route('/api/table/<int:places>', methods=['POST'])
async def create_table(places):
    """Функция создания стола в базе данных"""
    if places <= 0:
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    seats = []
    for i in range(1, places + 1):
        seats.append(f"{i}_True")
    seats = ";".join(seats)
    table = Tables(seats=seats)
    db_sess.add(table)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/take_place/<path:table_place>', methods=['POST'])
async def take_place(table_place):
    """Функция изменения занятости места за столом"""
    table, place = table_place.split("/")
    db_sess = db_session.create_session()
    try:
        table_inf = db_sess.query(Tables).get(table)
    except Exception:
        return jsonify({'error': 'Bad request'})
    places_inf = table_inf.seats
    places_inf = places_inf.split(";")
    try:
        place_change = places_inf[int(place) - 1].split("_")
    except Exception:
        return jsonify({'error': 'Bad request'})
    if place_change[1] == "True":
        place_change = "_".join([place_change[0], "False"])
    else:
        place_change = "_".join([place_change[0], "True"])
    places_inf[int(place) - 1] = place_change
    table_inf.seats = ";".join(places_inf)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/rating', methods=["POST"])
async def add_to_rating():
    json_data = request.json
    food_id, rate = json_data["food_id"], json_data["rate"]
    db_sess = db_session.create_session()
    food = db_sess.query(Food).get(food_id)
    cur_rating_inf: float = food.rating
    food.rating = (cur_rating_inf + int(rate)) / 2
    db_sess.commit()
    return jsonify({'success': 'OK'})