from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.log_utils.parsers.declare.declare_parsers import DeclareParser
from src.declare4py.models.log_generation.asp.asp_generator import AspGenerator

decl = """activity A
bind A: grade
bind A: mark, name
activity B
bind B: grade, mark, name
grade: integer between 1 and 5
mark: integer between 1 and 5
name: x, y, z, v
Existence [A] | | |
#Response[A, B] |A.grade > 2 |T.grade > 5 |1,5,s
Response[A, B] |A.grade > 2  | |1,5,s
Response[A, B] |A.grade < 2  | T.mark > 2|1,5,s
Chain Response[A, B] |A.grade < 2  | |1,5,s
"""

dp = DeclareParser()
d = dp.parse_from_string(decl)
# print(d)
# print(d.parsed_model.templates)

num_of_traces = 4
num_min_events = 2
num_max_events = 4


log_analyzer = LogAnalyzer()
asp = AspGenerator(
    num_of_traces,
    num_min_events,
    num_max_events,
    d,
    # "tests/files/declare/Response2.decl",
    # "tests/files/lp/templates.lp",
    # "tests/files/lp/generation_encoding.lp",
    log_analyzer,
)
#
asp.run()
asp.to_xes("../../generated_xes.xes")
