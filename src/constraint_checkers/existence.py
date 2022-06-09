from src.enums import *
from src.models import CheckerResult
from datetime import timedelta

# Defining global and local functions/variables to use within eval() to prevent code injection
glob = {'__builtins__': None}


# mp-existence constraint checker
# Description:
# The future constraining constraint existence(n, a) indicates that
# event a must occur at least n-times in the trace.
def mp_existence(trace, done, a, rules):
    activation_rules = rules["activation"]
    n = rules["n"][Template.EXISTENCE]
    time_rule = rules["time"]

    num_activations = 0
    T = trace[0]
    for A in trace:
        locl = {'A': A, 'T': T, 'timedelta': timedelta, 'abs': abs, 'float': float}
        if A["concept:name"] == a and eval(activation_rules, glob, locl):
            if eval(time_rule, glob, locl):
                num_activations += 1

    state = None
    if not done and num_activations < n:
        state = TraceState.POSSIBLY_VIOLATED
    elif done and num_activations < n:
        state = TraceState.VIOLATED
    elif num_activations >= n:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None, state=state)


# mp-absence constraint checker
# Description:
# The future constraining constraint absence(n + 1, a) indicates that
# event a may occur at most n − times in the trace.
def mp_absence(trace, done, a, rules):
    activation_rules = rules["activation"]
    n = rules["n"][Template.ABSENCE]
    time_rule = rules["time"]

    num_activations = 0
    T = trace[0]
    for A in trace:
        locl = {'A': A, 'T': T, 'timedelta': timedelta, 'abs': abs, 'float': float}
        if A["concept:name"] == a and eval(activation_rules, glob, locl):
            if eval(time_rule, glob, locl):
                num_activations += 1

    state = None
    if not done and num_activations < n:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_activations >= n:
        state = TraceState.VIOLATED
    elif done and num_activations < n:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None, state=state)


# mp-init constraint checker
# Description:
# The future constraining constraint init(e) indicates that
# event e is the first event that occurs in the trace.
def mp_init(trace, done, a, rules):
    activation_rules = rules["activation"]

    state = TraceState.VIOLATED
    if trace[0]["concept:name"] == a:
        A = trace[0]
        locl = {'A': A}
        if eval(activation_rules, glob, locl):
            state = TraceState.SATISFIED
    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None, state=state)


# mp-exactly constraint checker
# Description:
def mp_exactly(trace, done, a, rules):
    activation_rules = rules["activation"]
    n = rules["n"][Template.EXACTLY]
    time_rule = rules["time"]

    num_activations = 0
    T = trace[0]
    for A in trace:
        locl = {'A': A, 'T': T, 'timedelta': timedelta, 'abs': abs, 'float': float}
        if A["concept:name"] == a and eval(activation_rules, glob, locl):
            if eval(time_rule, glob, locl):
                num_activations += 1

    state = None
    if not done and num_activations < n:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_activations == n:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_activations > n or (done and num_activations < n):
        state = TraceState.VIOLATED
    elif done and num_activations == n:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=None, num_violations=None, num_pendings=None, num_activations=None, state=state)
