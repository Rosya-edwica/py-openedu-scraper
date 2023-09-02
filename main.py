import asyncio
import os
import sys
import time
import api
import db
from db import Database
import dotenv


ERROR_MESSAGE = "\n".join((
    "Программу нужно запускать с одним из следующих флагов:",
    "1. -postgres - для сохранения данных в Postgres",
    "2. -excel - для сохранения данных в Excel"
))

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        exit(ERROR_MESSAGE)

    match args[0]:
        case "-postgres":
            print("Данные будут сохранены в Postgres")
            asyncio.run(scrapeToPostgres())
        case "-excel":
            print("Данные будут сохранены в Excel")
            asyncio.run(scrapeToExcel())
        case _:
            exit(ERROR_MESSAGE)


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


async def scrapeToPostgres():
    courses = await api.get_all_courses()
    database = init_database()
    database.insert_many_courses(courses)
    database.close()


async def scrapeToExcel():
    courses = await api.get_all_courses()
    db.save_courses(courses)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    print(f"Time: {(time.perf_counter() - start_time) / 60} min.")
