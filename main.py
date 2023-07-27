import asyncio
import os
import time
import api
from db import Database
import dotenv


def init_database() -> Database:
    loaded = dotenv.load_dotenv(".env")
    if not loaded:
        exit("Создай файл .env с переменными окружения")
    database = Database(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        name=os.getenv("POSTGRES_DBNAME")
    )
    return database


async def main():
    courses = await api.get_all_courses()
    database = init_database()
    database.insert_many_courses(courses)
    database.close()


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Time: {(time.perf_counter() - start_time) / 60} min.")
