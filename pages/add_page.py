from __main__ import app
from flask import render_template
from flask_login import login_required
from forms.add import AddForm
from transliterate import translit
from aiohttp import ClientSession
import os


@app.route('/add', methods=['GET', 'POST'])
@login_required
async def add_page():
    """Обработка добавления блюда в меню"""
    type_converse = {'Первое': 'first', 'Второе': 'second', 'Салат': 'salads', 'Напиток': 'drinks', "Десерт": "desserts"}
    form = AddForm()
    msg = ""

    try:

        if form.validate_on_submit():
            text_id = translit(form.name.data.split()[0], language_code='ru', reversed=True).lower()
            session = ClientSession()
            await session.post(f"http://localhost:5000/api/food/none",
                 json={"name": form.name.data, "type": type_converse[form.type.data],
                       "composition": form.composition.data, "description": form.description.data,
                       "price": form.price.data, "text_id": text_id, "calories": form.calories.data,
                       "proteins": form.proteins.data, "fats": form.fats.data,
                       "carbohydrates": form.carb.data})
            img = form.image.data
            img.save(os.path.join(app.root_path, "static", "img", f"{text_id}.png"))
            await session.close()

    except Exception as e:
        msg = "При создании блюда произошла ошибка"
        print(e)

    return render_template('add.html', form=form, message=msg)