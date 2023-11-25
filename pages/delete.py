from __main__ import app
from flask import render_template
from forms.add import DeleteForm
from aiohttp import ClientSession


@app.route('/delete')
async def delete_page():
    session = ClientSession()
    form2 = DeleteForm()
    return render_template("delete.html", form2=form2)