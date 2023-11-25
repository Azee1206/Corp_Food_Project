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
        orders = db_sess.query(Order).all()
        all_orders_res = []
        for order in orders:
            order_num_res = order.order_number
            order_name_sur_res = order.name_sur
            order_status_res = "Готов" if order.is_done else "Готовится"
            cart_info = self.__load_cart(order.order_info).json
            order_info_res = cart_info["cart"]
            order_sum_res = cart_info["end_price"]
            order_res = {
                "order_num": order_num_res,
                "order_name_sur": order_name_sur_res,
                "order_status": order_status_res,
                "order_info": order_info_res,
                "order_sum": order_sum_res
            }
            all_orders_res.append(order_res)
        return jsonify(
            {
                "orders":
                    all_orders_res
            }
        )

    def __load_cart(self, cart):
        db_sess = db_session.create_session()
        cart = cart.split(";")
        cart_res = []
        end_price = 0
        for food_id in cart:
            if food_id:
                food_inf = db_sess.query(Food).get(food_id.split(".")[1])
                food_price = int(food_inf.price)
                food_amount = int(food_id.split(".")[0])
                food_id_res = food_id.split(".")[1]
                end_price = end_price + food_price * food_amount

                food_res = {"name": food_inf.name, "price": food_price,
                            "amount": food_amount, "food_id": food_id_res}
                cart_res.append(food_res)
        return jsonify(
            {
                "cart":
                    [item
                     for item in cart_res],
                "end_price": end_price
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
                'order': order.to_dict()
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
            client_id=request.json["client_id"],
            name_sur=request.json["name_sur"]
        )
        db_sess.add(order)
        db_sess.commit()
        return jsonify({'success': 'OK'})
