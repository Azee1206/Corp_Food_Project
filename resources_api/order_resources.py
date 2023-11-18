import dataclasses
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.user import User
from data.orders import Order
from flask import jsonify, request
from data.food_menu import Food


@dataclasses.dataclass
class OrderAllRecourse(Resource):
    def get(self):
        """Функция получения ВСЕХ блюд из базы данных"""
        db_sess = db_session.create_session()
        food = db_sess.query(Order).all()
        return jsonify(
            {
                "food":
                    [item.to_dict()
                     for item in food]
            }
        )


@dataclasses.dataclass
class OrderResource(Resource):
    def get(self, order_id):
        db_sess = db_session.create_session()
        order = db_sess.query(Order).get(order_id)
        if not order:
            return jsonify({'error': 'Not found'})
        return jsonify(
            {
                'food': order.to_dict()
            }
        )

    def post(self, order_id):
        db_sess = db_session.create_session()
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ["order_info", "client_id"]):
            return jsonify({'error': 'Bad request'})
        order = Order(
            order_info=request.json["order_info"],
            client_id=request.json["client_id"]
        )
        db_sess.add(order)
        db_sess.commit()
        return jsonify({'success': 'OK'})
