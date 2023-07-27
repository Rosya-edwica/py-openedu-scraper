import psycopg2
from psycopg2.extensions import connection
from models import Course


class Database:
    def __init__(self, host: str, port: int, user: str, password: str, name: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name
        self.connection = self.connect()

    def connect(self) -> connection:
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            dbname=self.name
        )
        return self.connection

    def close(self) -> None:
        self.connection.close()

    def insert_many_courses(self, courses: list[Course]) -> None:
        cursor = self.connection.cursor()

        query = """INSERT INTO course(
            organization, course_id, title, description,
            certificate, language, duration_in_weeks,
            url, start_date, cover_url, video_url, price,
            skills, module_program, program, platform
        ) VALUES(
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'openedu'
        ) ON CONFLICT DO NOTHING"""
        cursor.executemany(query, courses)
        self.connection.commit()
        print(f"Успешно сохранили {len(courses)} курсов")

