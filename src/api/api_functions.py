from src.constraint_checkers import *


def check_trace_conformance(trace, model, consider_vacuity):
    rules = {"vacuous_satisfaction": consider_vacuity}

    # Set containing all constraints that raised SyntaxError in checker functions
    error_constraint_set = set()

    trace_results = {}
    for constraint in model.checkers:
        constraint_str = constraint['template'].value
        if "n" in constraint:
            constraint_str += str(constraint['n'])
        constraint_str += '[' + constraint["attributes"] + '] |' + ' |'.join(constraint["condition"])

        rules["activation"] = constraint['condition'][0]
        rules["correlation"] = "True"   # set only when needed
        rules["time"] = constraint['condition'][-1]  # time condition is always at last position

        try:
            if constraint['template'] is Template.EXISTENCE:
                rules["n"] = constraint['n']
                trace_results[constraint_str] = mp_existence(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.ABSENCE:
                rules["n"] = constraint['n']
                trace_results[constraint_str] = mp_absence(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.INIT:
                trace_results[constraint_str] = mp_init(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.EXACTLY:
                rules["n"] = constraint['n']
                trace_results[constraint_str] = mp_exactly(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.CHOICE:
                trace_results[constraint_str] = mp_choice(trace, True, constraint['attributes'].split(', ')[0],
                                                          constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.EXCLUSIVE_CHOICE:
                trace_results[constraint_str] = mp_exclusive_choice(trace, True,
                                                                    constraint['attributes'].split(', ')[0],
                                                                    constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.RESPONDED_EXISTENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_responded_existence(trace, True,
                                                                       constraint['attributes'].split(', ')[0],
                                                                       constraint['attributes'].split(', ')[1], rules)
            
            elif constraint['template'] is Template.RESPONSE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_response(trace, True, constraint['attributes'].split(', ')[0],
                                                            constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.ALTERNATE_RESPONSE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_alternate_response(trace, True,
                                                                      constraint['attributes'].split(', ')[0],
                                                                      constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.CHAIN_RESPONSE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_chain_response(trace, True,
                                                                  constraint['attributes'].split(', ')[0],
                                                                  constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.PRECEDENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_precedence(trace, True, constraint['attributes'].split(', ')[0],
                                                              constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.ALTERNATE_PRECEDENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_alternate_precedence(trace, True,
                                                                        constraint['attributes'].split(', ')[0],
                                                                        constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.CHAIN_PRECEDENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_chain_precedence(trace, True,
                                                                    constraint['attributes'].split(', ')[0],
                                                                    constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_RESPONDED_EXISTENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_not_responded_existence(trace, True,
                                                                           constraint['attributes'].split(', ')[0],
                                                                           constraint['attributes'].split(', ')[1],
                                                                           rules)

            elif constraint['template'] is Template.NOT_RESPONSE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_not_response(trace, True, constraint['attributes'].split(', ')[0],
                                                                constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_CHAIN_RESPONSE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_not_chain_response(trace, True,
                                                                      constraint['attributes'].split(', ')[0],
                                                                      constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_PRECEDENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_not_precedence(trace, True,
                                                                  constraint['attributes'].split(', ')[0],
                                                                  constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_CHAIN_PRECEDENCE:
                rules["correlation"] = constraint['condition'][1]
                trace_results[constraint_str] = mp_not_chain_precedence(trace, True,
                                                                        constraint['attributes'].split(', ')[0],
                                                                        constraint['attributes'].split(', ')[1], rules)

        except SyntaxError:
            if constraint_str not in error_constraint_set:
                error_constraint_set.add(constraint_str)
                print('Condition not properly formatted for constraint "' + constraint_str
                      + '". Skipping it in conformance checking.')

    return trace_results
