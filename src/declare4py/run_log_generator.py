from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.log_utils.parsers.declare.declare_parsers import DeclareParser
from src.declare4py.models.asp_generator import AspGenerator
import json


decl = """activity Driving_Test
bind Driving_Test: Driver, Grade
activity Getting_License
bind Getting_License: Driver
activity Resit
bind Resit: Driver, Grade
activity Test_Failed
bind Test_Failed: Driver
Driver: Fabrizio, Mike, Marlon, Raimundas
Grade: integer between 1 and 5
Response[Driving_Test, Getting_License] |A.Grade>2 | |
Response[Driving_Test, Resit] |A.Grade<=2 | |
Response[Driving_Test, Test_Failed] |A.Grade<=2 | |
"""
dp = DeclareParser()
d = dp.parse_from_string(decl)
# print(d)
# print(d.parsed_model)
print(json.dumps(d.parsed_model._dict, indent=4))


num_of_traces = 4
num_min_events = 2
num_max_events = 4


# log_analyzer = LogAnalyzer()
# asp = AspGenerator(
#     num_of_traces,
#     num_min_events,
#     num_max_events,
#     "tests/files/declare/Response2.decl",
#     "tests/files/lp/templates.lp",
#     "tests/files/lp/generation_encoding.lp",
#     log_analyzer,
# )
#
# asp.run()