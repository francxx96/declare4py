from src.parsers import *
from src.enums import Template
from src.mp_checkers_old.log import *

import pm4py


def run_all_mp_checkers(IN_LOG_PATH, IN_DECL_PATH):
    log = pm4py.read_xes(IN_LOG_PATH)
    input = parse_decl(IN_DECL_PATH)
    activities = input.activities
    trace_set = set()
    for trace in log:
        trace_set.add(trace.attributes["concept:name"])

    for key, conditions in input.checkers.items():
        if key.startswith(Template.EXISTENCE):
            trace_set = trace_set.intersection(mp_existence_checker(log, True, activities[0], conditions[0], conditions[1]))
        elif key.startswith(Template.ABSENCE):
            trace_set = trace_set.intersection(mp_absence_checker(log, True, activities[0], conditions[0], conditions[1]))
        elif key.startswith(Template.INIT):
            trace_set = trace_set.intersection(mp_init_checker(log, True, activities[0], conditions[0]))
        elif key.startswith(Template.EXACTLY):
            trace_set = trace_set.intersection(mp_exactly_checker(log, True, activities[0], conditions[0], conditions[1]))
        elif key.startswith(Template.CHOICE):
            trace_set = trace_set.intersection(mp_choice_checker(log, True, activities[0], activities[1], conditions[0]))
        elif key.startswith(Template.EXCLUSIVE_CHOICE):
            trace_set = trace_set.intersection(mp_exclusive_choice_checker(log, True, activities[0], activities[1], conditions[0]))
        elif key.startswith(Template.RESPONDED_EXISTENCE):
            trace_set = trace_set.intersection(mp_responded_existence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.RESPONSE):
            trace_set = trace_set.intersection(mp_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.ALTERNATE_RESPONSE):
            trace_set = trace_set.intersection(mp_alternate_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.CHAIN_RESPONSE):
            trace_set = trace_set.intersection(mp_chain_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.PRECEDENCE):
            trace_set = trace_set.intersection(mp_precedence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.ALTERNATE_PRECEDENCE):
            trace_set = trace_set.intersection(mp_alternate_precedence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.CHAIN_PRECEDENCE):
            trace_set = trace_set.intersection(mp_chain_precedence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.ALTERNATE_RESPONSE):
            trace_set = trace_set.intersection(mp_alternate_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.NOT_RESPONSE):
            trace_set = trace_set.intersection(mp_not_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.NOT_CHAIN_RESPONSE):
            trace_set = trace_set.intersection(mp_not_chain_response_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.NOT_PRECEDENCE):
            trace_set = trace_set.intersection(mp_not_precedence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        elif key.startswith(Template.NOT_CHAIN_PRECEDENCE):
            trace_set = trace_set.intersection(mp_not_chain_precedence_checker(log, True, activities[0], activities[1], conditions[0], conditions[1]))
        print(trace_set)

        if len(trace_set) > 0:
            return True
        else:
            return False


run_all_mp_checkers("sepsis.xes", "sepsis.decl")
