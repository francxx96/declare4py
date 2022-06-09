from src.parsers import *
from src.constraint_checkers import *

import pm4py


def run_all_mp_checkers_traces(log_path, decl_path, consider_vacuity):
    log = pm4py.read_xes(log_path)
    model = parse_decl(decl_path)
    rules = {"vacuous_satisfaction": consider_vacuity}

    true_counter = 0
    false_counter = 0

    # Set containing all constraints that raised SyntaxError in checker functions
    error_constraint_set = set()

    for trace in log:
        result = True
        for constraint in model.checkers:
            rules["activation"] = constraint['condition'][0]
            rules["correlation"] = "True"
            rules["time"] = constraint['condition'][-1]  # time condition is always at last position

            try:
                if constraint['key'].startswith(Template.EXISTENCE):
                    rules["n"] = {Template.EXISTENCE: constraint['condition'][1]}
                    result = result and mp_existence(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.ABSENCE):
                    rules["n"] = {Template.ABSENCE: constraint['condition'][1]}
                    result = result and mp_absence(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.INIT):
                    result = result and mp_init(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.EXACTLY):
                    rules["n"] = {Template.EXACTLY: constraint['condition'][1]}
                    result = result and mp_exactly(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.CHOICE):
                    result = result and mp_choice(trace, True, constraint['attribute'].split(', ')[0],
                                                  constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.EXCLUSIVE_CHOICE):
                    result = result and mp_exclusive_choice(trace, True, constraint['attribute'].split(', ')[0],
                                                            constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.RESPONDED_EXISTENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_responded_existence(trace, True, constraint['attribute'].split(', ')[0],
                                                               constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_response(trace, True, constraint['attribute'].split(', ')[0],
                                                    constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.ALTERNATE_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_alternate_response(trace, True, constraint['attribute'].split(', ')[0],
                                                              constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.CHAIN_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_chain_response(trace, True, constraint['attribute'].split(', ')[0],
                                                          constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                      constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.ALTERNATE_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_alternate_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                                constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.CHAIN_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_chain_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                            constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_RESPONDED_EXISTENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_not_responded_existence(trace, True, constraint['attribute'].split(', ')[0],
                                                                   constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_not_response(trace, True, constraint['attribute'].split(', ')[0],
                                                        constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_CHAIN_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_not_chain_response(trace, True, constraint['attribute'].split(', ')[0],
                                                              constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_not_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                          constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_CHAIN_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    result = result and mp_not_chain_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                                constraint['attribute'].split(', ')[1], rules)

            except SyntaxError:
                constraint_str = constraint["key"] + "[" + constraint['attribute'].split(', ')[0] \
                                 + ", " + constraint['attribute'].split(', ')[1] + "]"

                if constraint_str not in error_constraint_set:
                    error_constraint_set.add(constraint_str)
                    print('Condition not properly formatted for constraint "'
                          + constraint_str + '". Skipping it in conformance checking.')

        if result:
            true_counter += 1
        else:
            false_counter += 1

    print("True: " + str(true_counter) + "\nFalse: " + str(false_counter))
    return result


run_all_mp_checkers_traces("Sepsis Cases.xes.gz", "sepsis model.decl", True)
