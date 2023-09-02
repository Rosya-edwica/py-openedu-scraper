from typing import NamedTuple


class Course(NamedTuple):
    Platform: str
    UniversityName: str
    # Id: str
    Title: str
    Description: str
    Certification: bool
    Duration: int | None
    Language: str
    Url: str
    StartDate: str
    Cover: str
    Video: str
    Price: int
    Skills: str
    IsModule: bool
    Program: str
