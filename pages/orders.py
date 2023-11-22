from __main__ import app
from flask import render_template
import aiohttp


@app.route('/orders')
async def orders_page():
    session = aiohttp.ClientSession()
    orders = await session.get(f"http://localhost:5000/api/all_orders")
    orders_json = await orders.json()
    orders_json = orders_json["orders"]
    return render_template("orders.html", orders=orders_json)
