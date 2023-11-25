from __main__ import app
from flask import render_template
from aiohttp import ClientSession


DAYS = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}


@app.route('/statistics/<statistics_type>')
async def statistics_page(statistics_type):
    session = ClientSession()
    if statistics_type == 'month':
        quarter_stat_list_resp = await session.get("http://localhost:5000/api/month_stat")
        await session.close()
        quarter_stat_list_json = await quarter_stat_list_resp.json()
        quarter_stat_list = quarter_stat_list_json["statistics"]
        return render_template("statistics_month.html", stat_list=quarter_stat_list)
    if statistics_type == 'day':
        all_stat_list_resp = await session.get("http://localhost:5000/api/all_stat")
        await session.close()
        all_stat_list_json = await all_stat_list_resp.json()
        all_stat_list = all_stat_list_json["statistics"]
        return render_template("statistics_day.html", stat_list=all_stat_list, days=DAYS)