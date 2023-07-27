from typing import NamedTuple


class Course(NamedTuple):
    UniversityName: str
    Id: str
    Title: str
    Description: str
    Certification: bool
    Language: str
    Duration: int | None
    Url: str
    StartDate: str
    Cover: str
    Video: str
    Price: int
    Skills: str
    IsModule: bool
    Program: str
