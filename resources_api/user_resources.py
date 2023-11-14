import dataclasses
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.user import User
from flask import jsonify
from data.food_menu import Food
from flask import request


@dataclasses.dataclass
class UserCartResource(Resource):
    def get(self, user_id):
        """Функция получения и представления в удобном виде данных о корзине пользователя"""
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if not user:
            return jsonify({'error': 'Not found'})
        cart = user.cart.split(";")
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

    def post(self, user_id):
        """Функция добавления и удаления (отрицательное добавление) блюд в корзину пользователя"""
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)

        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ["food_id", "amount"]):
            return jsonify({'error': 'Bad request'})

        food_id = request.json["food_id"]
        amount = request.json["amount"]
        if not user or not db_sess.query(Food).get(food_id) or amount == 0:
            return jsonify({'error': 'Not found'})

        cart = user.cart

        if food_id in cart:
            cart = cart.split(";")
            res_cart = []
            for elem in cart:
                if elem:
                    amount_current, food_id_current = elem.split(".")
                    res_cart.append(amount_current)
                    res_cart.append(food_id_current)
            food_indx = res_cart.index(food_id)
            res_cart[food_indx - 1] = str(int(res_cart[food_indx - 1]) + amount)

            if int(res_cart[food_indx - 1]) <= 0:
                del res_cart[food_indx - 1:food_indx + 1]

            point_symbol_flag = True
            res = ""
            for elem in res_cart:
                if point_symbol_flag:
                    res = res + elem + "."
                    point_symbol_flag = False
                else:
                    res = res + elem + ";"
                    point_symbol_flag = True

            user.cart = res
            db_sess.commit()

            return jsonify({'success': 'OK'})

        cart += f"{amount}.{food_id};"
        user.cart = cart
        db_sess.commit()

        return jsonify({'success': 'OK'})


@dataclasses.dataclass
class UserPaymentResource(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        payment_info = ["", "", ""]
        if user.payment_inf:
            payment_info = user.payment_inf.split(';')
        return jsonify(
            {"result": payment_info}
        )

    def post(self, user_id):
        json_data = request.json

        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ["number", "term", "cvc"]):
            return jsonify({'error': 'Bad request'})

        number = json_data["number"]
        term = json_data["term"]
        cvc = json_data["cvc"]

        if (not number.isdigit()) or (len(number) not in {13, 15, 16, 18, 19}):
            msg = "Некорректный формат номера карты"
            return jsonify({"msg": msg})

        if "/" not in term:
            msg = "Некорректный формат срока годности карты"
            return jsonify({"msg": msg})
        term = term.split("/")
        if (not term[0].isdigit()) or (not term[1].isdigit()):
            msg = "Некорректный формат срока годности карты"
            return jsonify({"msg": msg})

        if not cvc.isdigit() or len(cvc) != 3:
            msg = "Некорректный формат cvc кода"
            return jsonify({"msg": msg})

        info = f"{number};{term[0]}/{term[1]};{cvc}"
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        user.payment_inf = info
        db_sess.commit()
        msg = ""
        return jsonify({"msg": msg})


@dataclasses.dataclass
class UserHistoryResource(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        hist_str_inf: str = db_sess.query(User).get(user_id).history

        hist = hist_str_inf.split(",")

        res = []

        for order in hist:
            order_res = []
            for pare in order.split(";"):
                info = tuple(pare.split("."))
                if not info[0] or not info[1]:
                    continue
                order_res.append(info)
            res.append(order_res)

        return jsonify(
            {
                'history': res
            }
        )

    def post(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        hist = user.history
        if hist:
            hist = f"{hist},{user.cart}"
        else:
            hist = f"{user.cart}"
        user.history = hist
        user.cart = ""
        db_sess.commit()
        return jsonify({'success': 'OK'})

