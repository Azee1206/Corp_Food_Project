from __main__ import app
from flask import redirect, render_template
from flask_login import login_required, current_user
import aiohttp


@app.route('/food_delete/<path:inf>', methods=['GET', 'POST'])
@login_required
async def delete_food_from_cart(inf):

    """Удаления блюда из корзины"""

    session = aiohttp.ClientSession()
    usr_id, food_id, amount = inf.split("/")
    await session.post(f"http://localhost:5000/api/user/cart/{usr_id}",
                       json={"food_id": food_id, "amount": -int(amount)})
    await session.close()

    return redirect('/basket')


@app.route('/basket', methods=['GET', "POST"])
@login_required
async def basket_page():

    """Обработка корзины"""

    session = aiohttp.ClientSession()
    food_list_response = await session.get(f"http://localhost:5000/api/user/cart/{current_user.id}")
    food_list = await food_list_response.json()
    empty = False
    if len(food_list["cart"]) == 0:
        empty = True
    return render_template('basket.html', food_list=food_list, cur_usr=current_user, empty=empty)
