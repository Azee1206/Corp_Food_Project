import dataclasses
import datetime

from flask_restful import Resource
from data import db_session
from flask import request, jsonify
from data.statistics import Statistics
from data.statistics_quarter import StatisticsQuarter


@dataclasses.dataclass
class AllStatisticsResources(Resource):
    def get(self):
        db_sess = db_session.create_session()
        stat = db_sess.query(Statistics).order_by(-Statistics.num_of_sales).all()
        return jsonify(
            {
                "statistics":
                    [item.to_dict(only=("food_name", "num_of_sales", "day", "time"))
                     for item in stat]
            }
        )


@dataclasses.dataclass
class StatisticResources(Resource):
    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ["cart"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        cart: list[str] = request.json["cart"].split(";")[:-1]
        for pare in cart:
            print(pare)
            amount, text_id = pare.split(".")
            print(amount, text_id)
            amount = int(amount)
            stat: Statistics = db_sess.query(Statistics).get(text_id)
            print(stat)
            stat.num_of_sales += amount
            day = datetime.datetime.now().weekday() + 1
            hour = datetime.datetime.now().hour
            if not stat.day:
                stat.day = day
            else:
                stat.day = round((day + stat.day) / 2)
            if not stat.time:
                stat.time = hour
            else:
                stat.time = round((hour + stat.time) / 2)

            month_stat: StatisticsQuarter = db_sess.query(StatisticsQuarter).get(text_id)

            month_now = datetime.datetime.now().month

            match month_now:
                case 1:
                    month_stat.first_quarter += amount
                case 2:
                    month_stat.first_quarter += amount
                case 3:
                    month_stat.first_quarter += amount
                case 4:
                    month_stat.second_quarter += amount
                case 5:
                    month_stat.second_quarter += amount
                case 6:
                    month_stat.second_quarter += amount
                case 7:
                    month_stat.third_quarter += amount
                case 8:
                    month_stat.third_quarter += amount
                case 9:
                    month_stat.third_quarter += amount
                case 10:
                    month_stat.fourth_quarter += amount
                case 11:
                    month_stat.fourth_quarter += amount
                case 12:
                    month_stat.fourth_quarter += amount

        db_sess.commit()
        return jsonify({'success': 'OK'})


@dataclasses.dataclass
class StatisticsQuarterResources(Resource):
    def get(self):
        db_sess = db_session.create_session()
        stat = db_sess.query(StatisticsQuarter).all()
        return jsonify(
            {
                "statistics":
                    [item.to_dict(only=("food_name", "first_quarter",
                                        "second_quarter", "third_quarter", "fourth_quarter"))
                     for item in stat]
            }
        )


@dataclasses.dataclass
class StatisticsAdd(Resource):
    def post(self):
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ["text_id", "food_name"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        stat = Statistics(
            text_id=request["text_id"],
            food_name=request["food_name"]
        )
        month_stat = StatisticsQuarter(
            text_id=request["text_id"],
            food_name=request["food_name"]
        )
        db_sess.add(stat)
        db_sess.add(month_stat)
