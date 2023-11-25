from __main__ import app
from flask import render_template
from flask_login import current_user
from forms.payment import PaymentForm
import aiohttp


@app.route('/payment/<path:table_places_date_time>', methods=['GET', 'POST'])
async def payment_page(table_places_date_time):
    form_payment = PaymentForm()
    if form_payment.validate_on_submit():
        if (not form_payment.number.data.isdigit()) or (len(form_payment.number.data) not in {13, 15, 16, 18, 19}):
            msg = "Некорректный формат номера карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        term = form_payment.term.data
        if "/" not in term:
            msg = "Некорректный формат срока годности карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        term = term.split("/")
        if (not term[0].isdigit()) or (not term[1].isdigit()):
            msg = "Некорректный формат срока годности карты"
            return render_template("payment.html", form_payment=form_payment, message=msg)
        if not form_payment.cvc.data.isdigit() or len(form_payment.cvc.data) != 3:
            msg = "Некорректный формат cvc кода"
            return render_template("payment.html", form_payment=form_payment, message=msg)
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
        return render_template("basket.html", message=msg, food_list=[])
    return render_template("payment.html", form_payment=form_payment)
