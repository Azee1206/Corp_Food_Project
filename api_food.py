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


@blueprint.route('/api/table_one/<table_id>', methods=['GET'])
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


@blueprint.route('/api/create_table/<int:places>', methods=['POST'])
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