import dataclasses
from flask import jsonify
from flask_restful import Resource
from data import db_session
from data.tabels import Tables
from data.table_places_taken import TakenPlace


@dataclasses.dataclass
class AllTableResources(Resource):
    def get(self):
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


@dataclasses.dataclass
class TableResource(Resource):
    def post(self, table_places_date_time: str):
        """Функция изменения занятости места за столом"""
        table_id, places, date, time = table_places_date_time.split("/")
        places = places.split(",")
        db_sess = db_session.create_session()
        try:
            table_inf = db_sess.query(Tables).get(table_id)
        except Exception:
            return jsonify({'error': 'Bad request'})
        places_inf = table_inf.seats
        places_inf = places_inf.split(";")
        for place in places:
            try:
                place_change = places_inf[int(place) - 1].split("_")
            except Exception:
                return jsonify({'error': 'Bad request'})
            place_change = "_".join([place_change[0], "False"])
            places_inf[int(place) - 1] = place_change
            taken_place = TakenPlace(
                table_place_info=f"{table_id}_{place}",
                date=date,
                time=time
            )
            db_sess.add(taken_place)
        table_inf.seats = ";".join(places_inf)
        db_sess.commit()
        return jsonify({'success': 'OK'})
