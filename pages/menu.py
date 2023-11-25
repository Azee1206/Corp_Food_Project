from __main__ import app
from flask import redirect, render_template
from flask_login import current_user, login_required
import aiohttp


@app.route('/menu/rate/<path:info>')
async def rate_food(info):
    session = aiohttp.ClientSession()
    # первый элемент info - тип блюда, второй - оценка, третий - id оцениваемого блюда
    info = info.split("/")
    food_type = info[0]
    await session.post(f"http://localhost:5000/api/food/rating", json={"food_id": info[2], "rate": info[1]})
    await session.close()
    return redirect(f'/menu/{food_type}')


@app.route('/food_add/<path:inf>', methods=['GET', 'POST'])
@login_required
async def add_food_to_cart(inf):

    """Добавление блюда в корзину"""

    session = aiohttp.ClientSession()
    usr_id, food_id, food_type = inf.split("/")
    await session.post(f"http://localhost:5000/api/user/cart/{usr_id}",
                       json={"food_id": food_id, "amount": 1})
    await session.close()

    return redirect(f'/menu/{food_type}')


@app.route('/menu/<food_type>')
async def menu_page(food_type):

    """Обработка страницы меню"""

    session = aiohttp.ClientSession()

    food_list_response = await session.get(f'http://localhost:5000/api/food_all/1/{food_type}')
    food_list_json = await food_list_response.json()
    food_list = food_list_json["food"]
    await session.close()

    if current_user.is_authenticated:
        if current_user.role == 'admin':
            food_list.append('add')
    return render_template('menu.html', food_list=food_list, cur_usr=current_user)
