from __main__ import app
from flask import render_template, request, redirect
from flask_login import current_user
from forms.book_date import BookForm
import datetime
import aiohttp


@app.route("/pay_if_payment_info/<path:table_places_date_time>", methods=["GET", "POST"])
async def pay_if_payment_info(table_places_date_time: str):

    session = aiohttp.ClientSession()
    await session.post(f"http://localhost:5000/api/stat", json={"cart": current_user.cart})
    await session.post(f"http://localhost:5000/api/user/history/{current_user.id}")
    await session.post(f"http://localhost:5000/api/table/{table_places_date_time}")
    name_sur_info = await session.get(f"http://localhost:5000/api/user/name_sur/{current_user.id}")
    name_sur_json = await name_sur_info.json()
    name_sur = f"{name_sur_json['name']} {name_sur_json['sur']}"
    await session.post("http://localhost:5000/api/orders/none",
                       json={"order_info": current_user.cart,
                             "client_id": current_user.id,
                             "name_sur": name_sur})
    await session.close()

    msg = "Оплата проведена успешно"
    return render_template("basket.html", message=msg, food_list=[], empty=True)


async def get_booked_places(form):
    selected_places = []
    for field_name, field in form._fields.items():
        if field_name.startswith('place') and field.data:
            place_number = field_name.replace('place', '')
            selected_places.append(place_number)

    return selected_places


@app.route('/book', methods=['GET', 'POST'])
async def book_page():
    """Обработка страницы бронирования"""
    form_book = BookForm()
    time_choices = []
    current_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=19)

    while current_time <= end_time:
        time_choices.append((current_time.strftime('%H:%M'), current_time.strftime('%H:%M')))
        current_time += datetime.timedelta(minutes=15)

    form_book.time.choices = time_choices
    msg = ""
    session = aiohttp.ClientSession()
    table_list_resp = await session.get('http://localhost:5000/api/all_tables')
    await session.close()
    table_list_json = await table_list_resp.json()
    table_list = table_list_json['tables']
    table12_list = [i for i in table_list if len(i['seats'].split(';')) == 12]
    table6_list = [i for i in table_list if len(i['seats'].split(';')) == 6]

    if form_book.validate_on_submit():
        places = await get_booked_places(form_book)
        if not places:
            return render_template('book.html', message=msg, form_book=form_book,
                                   table12_list=table12_list, table6_list=table6_list, cur_usr=current_user)
        if "submit_payment" in request.form:
            places = ",".join(places)
            table_id = request.form.get('table_id')
            selected_date = form_book.date.data
            selected_time = form_book.time.data
            return redirect(f"/payment/{table_id}/{places}/{selected_date}/{selected_time}")
        if "submit_payment_if_info" in request.form:
            places = ",".join(places)
            table_id = request.form.get('table_id')
            selected_date = form_book.date.data
            selected_time = form_book.time.data
            return redirect(f"/pay_if_payment_info/{table_id}/{places}/{selected_date}/{selected_time}")

    return render_template('book.html', message=msg, form_book=form_book,
                           table12_list=table12_list, table6_list=table6_list, cur_usr=current_user)
