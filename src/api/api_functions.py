from src.constraint_checkers import *


def conformance_checking(log, model, consider_vacuity):
    rules = {"vacuous_satisfaction": consider_vacuity}

    # Set containing all constraints that raised SyntaxError in checker functions
    error_constraint_set = set()

    log_results = {}
    for i in range(len(log)):
        trace = log[i]
        trace_results = {}
        for constraint in model.checkers:
            constraint_str = constraint["key"] + '[' + constraint["attribute"] + '] |' + ' |'.join(
                constraint["condition"])

            rules["activation"] = constraint['condition'][0]
            rules["correlation"] = "True"
            rules["time"] = constraint['condition'][-1]  # time condition is always at last position

            try:
                if constraint['key'].startswith(Template.EXISTENCE):
                    rules["n"] = {Template.EXISTENCE: constraint['n']}
                    trace_results[constraint_str] = mp_existence(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.ABSENCE):
                    rules["n"] = {Template.ABSENCE: constraint['n']}
                    trace_results[constraint_str] = mp_absence(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.INIT):
                    trace_results[constraint_str] = mp_init(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.EXACTLY):
                    rules["n"] = {Template.EXACTLY: constraint['n']}
                    trace_results[constraint_str] = mp_exactly(trace, True, constraint['attribute'], rules)

                elif constraint['key'].startswith(Template.CHOICE):
                    trace_results[constraint_str] = mp_choice(trace, True, constraint['attribute'].split(', ')[0],
                                                              constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.EXCLUSIVE_CHOICE):
                    trace_results[constraint_str] = mp_exclusive_choice(trace, True,
                                                                        constraint['attribute'].split(', ')[0],
                                                                        constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.RESPONDED_EXISTENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_responded_existence(trace, True,
                                                                           constraint['attribute'].split(', ')[0],
                                                                           constraint['attribute'].split(', ')[1],
                                                                           rules)

                elif constraint['key'].startswith(Template.RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_response(trace, True, constraint['attribute'].split(', ')[0],
                                                                constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.ALTERNATE_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_alternate_response(trace, True,
                                                                          constraint['attribute'].split(', ')[0],
                                                                          constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.CHAIN_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_chain_response(trace, True,
                                                                      constraint['attribute'].split(', ')[0],
                                                                      constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_precedence(trace, True, constraint['attribute'].split(', ')[0],
                                                                  constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.ALTERNATE_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_alternate_precedence(trace, True,
                                                                            constraint['attribute'].split(', ')[0],
                                                                            constraint['attribute'].split(', ')[1],
                                                                            rules)

                elif constraint['key'].startswith(Template.CHAIN_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_chain_precedence(trace, True,
                                                                        constraint['attribute'].split(', ')[0],
                                                                        constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_RESPONDED_EXISTENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_not_responded_existence(trace, True,
                                                                               constraint['attribute'].split(', ')[0],
                                                                               constraint['attribute'].split(', ')[1],
                                                                               rules)

                elif constraint['key'].startswith(Template.NOT_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_not_response(trace, True, constraint['attribute'].split(', ')[0],
                                                                    constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_CHAIN_RESPONSE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_not_chain_response(trace, True,
                                                                          constraint['attribute'].split(', ')[0],
                                                                          constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_not_precedence(trace, True,
                                                                      constraint['attribute'].split(', ')[0],
                                                                      constraint['attribute'].split(', ')[1], rules)

                elif constraint['key'].startswith(Template.NOT_CHAIN_PRECEDENCE):
                    rules["correlation"] = constraint['condition'][1]
                    trace_results[constraint_str] = mp_not_chain_precedence(trace, True,
                                                                            constraint['attribute'].split(', ')[0],
                                                                            constraint['attribute'].split(', ')[1],
                                                                            rules)

            except SyntaxError:
                if constraint_str not in error_constraint_set:
                    error_constraint_set.add(constraint_str)
                    print('Condition not properly formatted for constraint "'
                          + constraint_str + '". Skipping it in conformance checking.')

        log_results[(i, trace.attributes["concept:name"])] = trace_results

    return log_results
