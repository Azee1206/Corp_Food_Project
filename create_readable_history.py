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
