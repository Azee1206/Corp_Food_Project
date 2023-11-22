from __main__ import app
from flask import render_template


@app.route("/")
async def default_page():
    """Обработка главной страницы"""
    return render_template("main.html")
