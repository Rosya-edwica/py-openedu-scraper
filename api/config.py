import os

import aiohttp
import dotenv

env_loaded = dotenv.load_dotenv(".env")
if not env_loaded:
    exit("Создай файл .env с переменными окружения")

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


async def get_json(url: str) -> dict:
    global ACCESS_TOKEN
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    print(f"Выполняется запрос к {url} ...",)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 401:
                ACCESS_TOKEN = await update_access_token()
                return await get_json(url)
            else:
                data = await response.json()
                return data


async def update_access_token() -> str | None:
    URL = "https://openedu.ru/api/catalog_export/v0/authorize"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(URL, json=data) as response:
            if response.status == 200:
                data = await response.json()
                token = data["accessToken"]
                dotenv.set_key(".env", "ACCESS_TOKEN", token)
                return token
            else:
                return None
