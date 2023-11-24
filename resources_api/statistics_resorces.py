import dataclasses
import datetime

from flask_restful import Resource
from data import db_session
from flask import request, jsonify
from data.statistics import Statistics
from data.statistics_month import StatisticsMonth


@dataclasses.dataclass
class AllStatisticsResources(Resource):
    def get(self):
        db_sess = db_session.create_session()
        stat = db_sess.query(Statistics).all()
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
                     ["day", "time", "cart"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        cart: list[str] = request.json["cart"].split(";")
        for pare in cart:
            amount, food_id = pare.split(".")
            stat: Statistics = db_sess.query(Statistics).get(food_id)
            stat.num_of_sales += amount
            if not stat.day:
                stat.day = request.json["day"]
            else:
                stat.day = round((request.json["day"] + stat.day) / 2)
            if not stat.time:
                stat.time = request.json["time"]
            else:
                stat.time = round((request.json["time"] + stat.time) / 2)

            month_stat: StatisticsMonth = db_sess.query(StatisticsMonth).get(food_id)

            month_now = datetime.datetime.now().month

            match month_now:
                case 1:
                    month_stat.january += amount
                case 2:
                    month_stat.february += amount
                case 3:
                    month_stat.march += amount
                case 4:
                    month_stat.april += amount
                case 5:
                    month_stat.may += amount
                case 6:
                    month_stat.june += amount
                case 7:
                    month_stat.july += amount
                case 8:
                    month_stat.august += amount
                case 9:
                    month_stat.september += amount
                case 10:
                    month_stat.october += amount
                case 11:
                    month_stat.november += amount
                case 12:
                    month_stat.december += amount

        db_sess.commit()
        return jsonify({'success': 'OK'})


@dataclasses.dataclass
class StatisticsMonthResources(Resource):
    def get(self, quarter):
        db_sess = db_session.create_session()
        stat = db_sess.query(StatisticsMonth).get().all()
        match quarter:
            case 1:
                return jsonify(
                    {
                        "statistics":
                            [item.to_dict(only=("january", "february", "march"))
                             for item in stat]
                    }
                )
            case 2:
                return jsonify(
                    {
                        "statistics":
                            [item.to_dict(only=("april", "may", "june"))
                             for item in stat]
                    }
                )
            case 3:
                return jsonify(
                    {
                        "statistics":
                            [item.to_dict(only=("july", "august", "september"))
                             for item in stat]
                    }
                )
            case 4:
                return jsonify(
                    {
                        "statistics":
                            [item.to_dict(only=("october", "november", "december"))
                             for item in stat]
                    }
                )