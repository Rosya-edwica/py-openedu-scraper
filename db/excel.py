import pandas as pd
from models import Course

TABLE_COLUMNS = (
    "Организатор курса",
    "Организатор вуз",
    "Название курса",
    "Описание курса",
    "Сертификат",
    "Продолжительность в неделях",
    "Язык",
    "Ссылка на страницу",
    "Дата начала",
    "Обложка курса",
    "Видео",
    "Цена",
    "Навыки",
    "Модульный курс",
    "Программа"
)

def save_courses(courses: list[Course]) -> None:
    unpacked_data = [[*course] for course in courses]
    data = pd.DataFrame(data=unpacked_data, columns=TABLE_COLUMNS)
    data.to_csv("courses.csv", index=False)