from __main__ import app
from flask import render_template
from flask_login import current_user
from forms.payment import PaymentForm
import aiohttp


async def create_readable_history(history: list[list[str]]) -> list[list[tuple]]:
    history_res = []
    session = aiohttp.ClientSession()
    for order in history:
        order_res = []
        for item in order:
            food_name_request = await session.get(f"http://localhost:5000/api/food/{item[1]}")
            food_name_json = await food_name_request.json()
            try:
                food = food_name_json["food"]
                food_name = food["name"]
            except KeyError:
                food_name = "ошибка в получении информации о блюде"
            order_res.append((item[0], food_name))
        history_res.append(order_res)
    return history_res


async def get_payment_inf(session):
    payment_inf_res = await session.get(f"http://localhost:5000/api/user/payment/{current_user.id}")
    payment_inf_json = await payment_inf_res.json()
    payment_inf = payment_inf_json["result"]
    payment_inf[0] = f"{payment_inf[0][:4]}{'*' * (len(payment_inf[0]) - 8)}{payment_inf[0][-4:]}"
    payment_inf[0] = str(payment_inf[0])
    payment_inf[2] = f"{payment_inf[2][0]}**"
    return payment_inf


@app.route("/profile", methods=['GET', 'POST'])
async def profile_page():

    """Обработка страницы профиля"""

    form = PaymentForm()

    session = aiohttp.ClientSession()

    if current_user.payment_inf:
        payment_inf = await get_payment_inf(session)
    else:
        payment_inf = ["", "", ""]

    history_result = await session.get(f"http://localhost:5000/api/user/history/{current_user.id}")
    history_json = await history_result.json()
    history = history_json["history"]
    history_res = await create_readable_history(history)

    if form.validate_on_submit():
        number = form.number.data
        term = form.term.data
        cvc = form.cvc.data

        msg_res = await session.post(f"http://localhost:5000/api/user/payment/{current_user.id}",
                           json={"number": number, "term": term, "cvc": cvc})

        msg_json = await msg_res.json()
        msg = msg_json["msg"]
        payment_inf = await get_payment_inf(session)
        await session.close()

        return render_template("profile.html", payment_inf=payment_inf, form_payment=form, history=history_res, message=msg)

    await session.close()
    return render_template("profile.html", payment_inf=payment_inf, form_payment=form, history=history_res)
