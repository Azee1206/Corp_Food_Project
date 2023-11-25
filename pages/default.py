from __main__ import app
from flask import render_template

from project.forms.voting import VoteForm


@app.route("/")
async def default_page():
    """Обработка главной страницы"""
    form = VoteForm()
    return render_template("main.html", form=form)
