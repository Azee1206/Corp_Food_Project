import dataclasses
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.food_menu import Food
from flask import request, jsonify


@dataclasses.dataclass
class FoodAllRecourse(Resource):
    def get(self, visible_foodtype: str):
        """Функция получения ВСЕХ блюд из базы данных"""
        db_sess = db_session.create_session()
        visible, food_type = visible_foodtype.split("/")
        if visible == "1":
            food = db_sess.query(Food).filter(Food.visible, Food.type == food_type).all()
        else:
            food = db_sess.query(Food).all()
        return jsonify(
            {
                "food":
                    [item.to_dict(only=
                                  ("name", "type", "composition", "description", "price", "visible", "text_id",
                                   "calories_proteins", "rating"))
                     for item in food]
            }
        )


@dataclasses.dataclass
class FoodRecourse(Resource):
    def get(self, food_id):
        """Функция получения ОДНОГО блюда из базы данных"""
        db_sess = db_session.create_session()
        food = db_sess.query(Food).get(food_id)
        if not food:
            return jsonify({'error': 'Not found'})
        return jsonify(
            {
                'food': food.to_dict(only=
                                     ("name", "type", "composition", "description", "price", "visible", "text_id",
                                      "calories_proteins"))
            }
        )

    def post(self, food_id):
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


@dataclasses.dataclass
class FoodRatingRecourse(Resource):
    def post(self):
        json_data = request.json
        food_id, rate = json_data["food_id"], json_data["rate"]
        db_sess = db_session.create_session()
        food = db_sess.query(Food).get(food_id)
        cur_rating_inf: float = food.rating
        food.rating = (cur_rating_inf + int(rate)) / 2
        db_sess.commit()
        return jsonify({'success': 'OK'})


@dataclasses.dataclass
class AllFoodNameRecourse(Resource):
    def get(self):
        db_sess = db_session.create_session()
        food_names = db_sess.query(Food.name).all()
        return jsonify(
            {
                "food":
                    [item.to_dict(only=
                                  ("name"))
                     for item in food_names]
            }
        )
