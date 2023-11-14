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