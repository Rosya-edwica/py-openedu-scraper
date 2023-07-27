import re
from typing import NamedTuple


class Module(NamedTuple):
    IsModule: bool
    DumpedProgram: str


def clear_tags(text: str) -> str:
    return re.sub("<.*?>|\xa0|\n|\t", "", text)


