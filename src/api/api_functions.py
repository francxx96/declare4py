from src.constraint_checkers import *
from src.models import DeclModel


def check_trace_conformance(trace, model, consider_vacuity):
    rules = {"vacuous_satisfaction": consider_vacuity}

    # Set containing all constraints that raised SyntaxError in checker functions
    error_constraint_set = set()

    trace_results = {}
    
    for constraint in model.checkers:
        constraint_str = constraint['template'].templ_str
        if constraint['template'].supports_cardinality:
            constraint_str += str(constraint['n'])
        constraint_str += '[' + constraint["attributes"] + '] |' + ' |'.join(constraint["condition"])

        rules["activation"] = constraint['condition'][0]

        if constraint['template'].supports_cardinality:
            rules["n"] = constraint['n']
        if constraint['template'].is_binary:
            rules["correlation"] = constraint['condition'][1]

        rules["time"] = constraint['condition'][-1]  # time condition is always at last position

        try:
            if constraint['template'] is Template.EXISTENCE:
                trace_results[constraint_str] = mp_existence(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.ABSENCE:
                trace_results[constraint_str] = mp_absence(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.INIT:
                trace_results[constraint_str] = mp_init(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.EXACTLY:
                trace_results[constraint_str] = mp_exactly(trace, True, constraint['attributes'], rules)

            elif constraint['template'] is Template.CHOICE:
                trace_results[constraint_str] = mp_choice(trace, True, constraint['attributes'].split(', ')[0],
                                                          constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.EXCLUSIVE_CHOICE:
                trace_results[constraint_str] = mp_exclusive_choice(trace, True,
                                                                    constraint['attributes'].split(', ')[0],
                                                                    constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.RESPONDED_EXISTENCE:
                trace_results[constraint_str] = mp_responded_existence(trace, True,
                                                                       constraint['attributes'].split(', ')[0],
                                                                       constraint['attributes'].split(', ')[1], rules)
            
            elif constraint['template'] is Template.RESPONSE:
                trace_results[constraint_str] = mp_response(trace, True, constraint['attributes'].split(', ')[0],
                                                            constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.ALTERNATE_RESPONSE:
                trace_results[constraint_str] = mp_alternate_response(trace, True,
                                                                      constraint['attributes'].split(', ')[0],
                                                                      constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.CHAIN_RESPONSE:
                trace_results[constraint_str] = mp_chain_response(trace, True,
                                                                  constraint['attributes'].split(', ')[0],
                                                                  constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.PRECEDENCE:
                trace_results[constraint_str] = mp_precedence(trace, True, constraint['attributes'].split(', ')[0],
                                                              constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.ALTERNATE_PRECEDENCE:
                trace_results[constraint_str] = mp_alternate_precedence(trace, True,
                                                                        constraint['attributes'].split(', ')[0],
                                                                        constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.CHAIN_PRECEDENCE:
                trace_results[constraint_str] = mp_chain_precedence(trace, True,
                                                                    constraint['attributes'].split(', ')[0],
                                                                    constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_RESPONDED_EXISTENCE:
                trace_results[constraint_str] = mp_not_responded_existence(trace, True,
                                                                           constraint['attributes'].split(', ')[0],
                                                                           constraint['attributes'].split(', ')[1],
                                                                           rules)

            elif constraint['template'] is Template.NOT_RESPONSE:
                trace_results[constraint_str] = mp_not_response(trace, True, constraint['attributes'].split(', ')[0],
                                                                constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_CHAIN_RESPONSE:
                trace_results[constraint_str] = mp_not_chain_response(trace, True,
                                                                      constraint['attributes'].split(', ')[0],
                                                                      constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_PRECEDENCE:
                trace_results[constraint_str] = mp_not_precedence(trace, True,
                                                                  constraint['attributes'].split(', ')[0],
                                                                  constraint['attributes'].split(', ')[1], rules)

            elif constraint['template'] is Template.NOT_CHAIN_PRECEDENCE:
                trace_results[constraint_str] = mp_not_chain_precedence(trace, True,
                                                                        constraint['attributes'].split(', ')[0],
                                                                        constraint['attributes'].split(', ')[1], rules)

        except SyntaxError:
            if constraint_str not in error_constraint_set:
                error_constraint_set.add(constraint_str)
                print('Condition not properly formatted for constraint "' + constraint_str
                      + '". Skipping it in conformance checking.')

    return trace_results


def discover_constraint(log, constraint, consider_vacuity):
    # Fake model composed by a single constraint
    model = DeclModel()
    model.checkers.append(constraint)

    discovery_res = {}

    for i, trace in enumerate(log):
        trc_res = check_trace_conformance(trace, model, consider_vacuity)

        for constraint_str, checker_res in trc_res.items():  # trc_res will always have only one element inside
            if checker_res.state == TraceState.SATISFIED:
                new_val = {(i, trace.attributes['concept:name']): checker_res}
                if constraint_str in discovery_res:
                    discovery_res[constraint_str] |= new_val
                else:
                    discovery_res[constraint_str] = new_val

    return discovery_res


def query_constraint(log, constraint, consider_vacuity, min_support):
    # Fake model composed by a single constraint
    model = DeclModel()
    model.checkers.append(constraint)

    discovery_res = {}

    for i, trace in enumerate(log):
        trc_res = check_trace_conformance(trace, model, consider_vacuity)
        
        for constraint_str, checker_res in trc_res.items():  # trc_res will always have only one element inside
            if checker_res.state == TraceState.SATISFIED:
                
                new_val = {(i, trace.attributes['concept:name']): checker_res}
                if constraint_str in discovery_res:
                    discovery_res[constraint_str] |= new_val
                else:
                    discovery_res[constraint_str] = new_val
                    
                if len(discovery_res[constraint_str]) / len(log) >= min_support:
                    break
        else:
            continue
        break
    return discovery_res
