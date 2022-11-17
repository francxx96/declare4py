from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.log_utils.parsers.declare.declare_parsers import DeclareParser
from src.declare4py.models.asp_generator import AspGenerator
import json


decl = """activity activity_1
bind activity_1: categorical, integer
activity activity_2
bind activity_2: categorical, integer
activity activity_3
bind activity_3: categorical, integer
activity activity_4
bind activity_4: categorical, integer
activity activity_5
bind activity_5: categorical, integer
activity activity_6
bind activity_6: categorical, integer
activity activity_7
bind activity_7: categorical, integer
activity activity_8
bind activity_8: categorical, integer
activity activity_9
bind activity_9: categorical, integer
activity activity_10
bind activity_10: categorical, integer
activity activity_11
bind activity_11: categorical, integer
activity activity_12
bind activity_12: categorical, integer
activity activity_13
bind activity_13: categorical, integer
activity activity_14
bind activity_14: categorical, integer
activity activity_15
bind activity_15: categorical, integer
activity activity_16
bind activity_16: categorical, integer
activity activity_17
bind activity_17: categorical, integer
categorical: c1, c2, c3
integer: integer between 0 and 100
Response[activity_1, activity_2] |A.integer > 10 |T.integer > 10 |
Chain Response[activity_3, activity_4] |A.categorical is c1 |T.categorical is c2 |
Absence[activity_5] |A.categorical is c3 |
Response[activity_6, activity_7] |A.integer > 10 |T.integer > 10 |
Chain Response[activity_8, activity_9] |A.categorical is c1 |T.categorical is c2 |
Existence[activity_10] |A.categorical is c3 |
Response[activity_11, activity_12] |A.integer > 10 |T.integer > 10 |
Chain Response[activity_13, activity_14] |A.categorical is c1 |T.categorical is c2 |
Existence[activity_15] |A.categorical is c3 |
Response[activity_16, activity_17] |A.integer > 10 |T.integer > 10 |
"""
dp = DeclareParser()
d = dp.parse_from_string(decl)
# print(d)
print(d.parsed_model.to_json())
# print(json.dumps(d.parsed_model, indent=4))


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