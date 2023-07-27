import re
import json

from program_tools.lessons import build_lesson_type
from program_tools.module import build_module_type
from program_tools.config import Module


def bring_program_to_single_structure(program: str) -> Module:
    if re.findall(r"Раздел |Тема \d+|Модуль |РАЗДЕЛ ", program):
        return Module(
            IsModule=True,
            DumpedProgram=json.dumps(build_module_type(program), ensure_ascii=False)
        )
    else:
        return Module(
            IsModule=False,
            DumpedProgram=json.dumps(build_lesson_type(program), ensure_ascii=False)
        )
