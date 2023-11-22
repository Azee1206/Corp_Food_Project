from datetime import datetime, timedelta
from data import db_session
from data.table_places_taken import TakenPlace
from data.tabels import Tables


def check_tables():
    current_datetime = datetime.now()
    db_sess = db_session.create_session()
    taken_places = db_sess.query(TakenPlace).all()

    for taken_place in taken_places:
        # Преобразуем строковые дату и время в объект datetime
        place_datetime = datetime.strptime(taken_place.date + " " + taken_place.time, "%Y-%m-%d %H:%M")

        # Проверяем, прошло ли 15 минут с момента занятия места
        if (current_datetime - place_datetime) >= timedelta(minutes=15):
            table_id, place = map(int, taken_place.table_place_info.split('_'))
            table = db_sess.query(Tables).filter(Tables.table_id == table_id).first()
            places_inf = table.seats
            places_inf = places_inf.split(";")
            place_change = places_inf[int(place) - 1].split("_")
            place_change = "_".join([place_change[0], "True"])
            places_inf[int(place) - 1] = place_change
            db_sess.add(taken_place)
            table.seats = ";".join(places_inf)
            db_sess.delete(taken_place)
            db_sess.commit()
