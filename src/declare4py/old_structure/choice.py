from ..enums import TraceState
from ..models import CheckerResult
from ..parsers import parse_data_cond, parse_time_cond
from datetime import timedelta

# Defining global and local functions/variables to use within eval() to prevent code injection
glob = {'__builtins__': None}


# mp-choice constraint checker
# Description:
def mp_choice(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    time_rule = parse_time_cond(rules["time"])

    a_or_b_occurs = False
    for A in trace:
        if A["concept:name"] == a or A["concept:name"] == b:
            locl = {'A': A, 'T': trace[0], 'timedelta': timedelta, 'abs': abs, 'float': float}
            if eval(activation_rules, glob, locl) and eval(time_rule, glob, locl):
                a_or_b_occurs = True
                break

    state = None
    if not done and not a_or_b_occurs:
        state = TraceState.POSSIBLY_VIOLATED
    elif done and not a_or_b_occurs:
        state = TraceState.VIOLATED
    elif a_or_b_occurs:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None,
                         state=state)


# mp-exclusive-choice constraint checker
# Description:
def mp_exclusive_choice(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    time_rule = parse_time_cond(rules["time"])

    a_occurs = False
    b_occurs = False
    for A in trace:
        locl = {'A': A, 'T': trace[0], 'timedelta': timedelta, 'abs': abs, 'float': float}
        if not a_occurs and A["concept:name"] == a:
            if eval(activation_rules, glob, locl) and eval(time_rule, glob, locl):
                a_occurs = True
        if not b_occurs and A["concept:name"] == b:
            if eval(activation_rules, glob, locl) and eval(time_rule, glob, locl):
                b_occurs = True
        if a_occurs and b_occurs:
            break

    state = None
    if not done and (not a_occurs and not b_occurs):
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and (a_occurs ^ b_occurs):
        state = TraceState.POSSIBLY_SATISFIED
    elif (a_occurs and b_occurs) or (done and (not a_occurs and not b_occurs)):
        state = TraceState.VIOLATED
    elif done and (a_occurs ^ b_occurs):
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None,
                         state=state)
