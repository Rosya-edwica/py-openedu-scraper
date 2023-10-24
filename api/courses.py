import api
import requests
import program_tools
from models import Course
from program_tools import bring_program_to_single_structure
import re


async def get_all_courses() -> list[Course]:
    courses: list[Course] = []
    page_num = 0
    courses_count = await get_courses_count()
    print("Количество курсов: ", courses_count) 
    while True:
        page_num += 1
        page_courses = await get_page_courses(page_num)
        if not page_courses:
            break
        courses += page_courses
    return courses


async def get_page_courses(page_num: int) -> list[Course]:
    courses: list[Course] = []
    url = f"https://openedu.ru/api/catalog_export/v0/catalog_courses?page={page_num}"
    page_json = await api.get_json(url)
    if not page_json["data"]:
        return []

    for item in page_json["data"]:
        course = get_course(item)
        courses.append(course)
    return courses

async def get_courses_count() -> int:
    url = f"https://openedu.ru/api/catalog_export/v0/catalog_courses"
    resp = await api.get_json(url)
    return resp["total"]


def get_course(course_json: dict) -> Course:
    program = course_json["syllabus"]
    if program:
        program = bring_program_to_single_structure(program)
        if not program.DumpedProgram:
            exit(f"нет программы: {course_json['syllabus']}")
    else:
        program = program_tools.Module(DumpedProgram="", IsModule=False)
    course = Course(
        Platform="Открытое образование",
        UniversityName=course_json["university_name"],
        Title=course_json["title"],
        # Id=course_json["id"],
        Description=clear_desription(course_json["description"]),
        Language=rename_language(course_json["lang"]),
        Cover=course_json["cover"],
        Video=course_json["video"],
        Program=program.DumpedProgram,
        Skills="|".join(clear_skills(course_json["result_skills"])),
        Url=course_json["url"],
        StartDate=course_json["start"],
        Price=course_json["price"],
        Duration=course_json["duration_to"],
        Certification=True,
        IsModule=program.IsModule
    )
    return course


def rename_language(lang: str) -> str:
    match lang:
        case "ru": return "Русский"
        case "en": return "Английский"
        case _: exit(f"Неопознанный язык {lang}")


def clear_skills(text: str) -> list[str]:
    items = re.findall(r"<li>.*?</li>", text)
    items = [re.sub(r"<li>|</li>|;|·;|· ", "", i) for i in items]
    return items


def clear_desription(text: str) -> str:
    text = re.sub(r"<table>|</table>|<tbody>|</tbody>|<tr>|</tr>|<td>|</td>|<a href.*?<\/a>", "", text)
    return text.strip()