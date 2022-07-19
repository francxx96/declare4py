from ..enums import TraceState
from ..models import CheckerResult
from ..parsers import parse_data_cond, parse_time_cond
from datetime import timedelta

# Defining global and local functions/variables to use within eval() to prevent code injection
glob = {'__builtins__': None}


# mp-responded-existence constraint checker
# Description:
# The future constraining and history-based constraint
# respondedExistence(a, b) indicates that, if event a occurs in the trace
# then event b occurs in the trace as well.
# Event a activates the constraint.
def mp_responded_existence(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    pendings = []
    num_fulfillments = 0
    num_violations = 0
    num_pendings = 0

    for event in trace:
        if event["concept:name"] == a:
            locl = {'A': event}
            if eval(activation_rules, glob, locl):
                pendings.append(event)

    for event in trace:
        if not pendings:
            break

        if event["concept:name"] == b:
            for A in reversed(pendings):
                locl = {'A': A, 'T': event, 'timedelta': timedelta, 'abs': abs, 'float': float}
                if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                    pendings.remove(A)
                    num_fulfillments += 1

    if done:
        num_violations = len(pendings)
    else:
        num_pendings = len(pendings)

    num_activations = num_fulfillments + num_violations + num_pendings
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif done and num_violations > 0:
        state = TraceState.VIOLATED
    elif done and num_violations == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings,
                         num_activations=num_activations, state=state)


# mp-response constraint checker
# Description:
# The future constraining constraint response(a, b) indicates that
# if event a occurs in the trace, then event b occurs after a.
# Event a activates the constraint.
def mp_response(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    pendings = []
    num_fulfillments = 0
    num_violations = 0
    num_pendings = 0

    for event in trace:
        if event["concept:name"] == a:
            locl = {'A': event}
            if eval(activation_rules, glob, locl):
                pendings.append(event)

        if pendings and event["concept:name"] == b:
            for A in reversed(pendings):
                locl = {'A': A, 'T': event, 'timedelta': timedelta, 'abs': abs, 'float': float}
                if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                    pendings.remove(A)
                    num_fulfillments += 1

    if done:
        num_violations = len(pendings)
    else:
        num_pendings = len(pendings)

    num_activations = num_fulfillments + num_violations + num_pendings
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_pendings > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_pendings == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif done and num_violations > 0:
        state = TraceState.VIOLATED
    elif done and num_violations == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings,
                         num_activations=num_activations, state=state)


# mp-alternate-response constraint checker
# Description:
# The future constraining constraint alternateResponse(a, b) indicates that
# each time event a occurs in the trace then event b occurs afterwards
# before event a recurs.
# Event a activates the constraint.
def mp_alternate_response(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    pending = None
    num_activations = 0
    num_fulfillments = 0
    num_pendings = 0

    for event in trace:
        if event["concept:name"] == a:
            locl = {'A': event}
            if eval(activation_rules, glob, locl):
                pending = event
                num_activations += 1

        if event["concept:name"] == b and pending is not None:
            locl = {'A': pending, 'T': event, 'timedelta': timedelta, 'abs': abs, 'float': float}
            if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                pending = None
                num_fulfillments += 1

    if not done and pending is not None:
        num_pendings = 1

    num_violations = num_activations - num_fulfillments - num_pendings
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0 and num_pendings > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0 and num_pendings == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations > 0 or (done and num_pendings > 0):
        state = TraceState.VIOLATED
    elif done and num_violations == 0 and num_pendings == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings,
                         num_activations=num_activations, state=state)


# mp-chain-response constraint checker
# Description:
# The future constraining constraint chain_response(a, b) indicates that,
# each time event a occurs in the trace, event b occurs immediately afterwards.
# Event a activates the constraint.
def mp_chain_response(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    num_activations = 0
    num_fulfillments = 0
    num_pendings = 0

    for index, event in enumerate(trace):

        if event["concept:name"] == a:
            locl = {'A': event}

            if eval(activation_rules, glob, locl):
                num_activations += 1

                if index < len(trace) - 1:
                    if trace[index+1]["concept:name"] == b:
                        locl = {'A': event, 'T': trace[index+1], 'timedelta': timedelta, 'abs': abs, 'float': float}
                        if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                            num_fulfillments += 1
                else:
                    if not done:
                        num_pendings = 1

    num_violations = num_activations - num_fulfillments - num_pendings
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0 and num_pendings > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0 and num_pendings == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations > 0 or (done and num_pendings > 0):
        state = TraceState.VIOLATED
    elif done and num_violations == 0 and num_pendings == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings,
                         num_activations=num_activations, state=state)


# mp-precedence constraint checker
# Description:
# The history-based constraint precedence(a,b) indicates that event b occurs
# only in the trace, if preceded by a. Event b activates the constraint.
def mp_precedence(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    num_activations = 0
    num_fulfillments = 0
    Ts = []

    for event in trace:
        if event["concept:name"] == a:
            Ts.append(event)

        if event["concept:name"] == b:
            locl = {'A': event}

            if eval(activation_rules, glob, locl):
                num_activations += 1

                for T in Ts:
                    locl = {'A': event, 'T': T, 'timedelta': timedelta, 'abs': abs, 'float': float}
                    if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                        num_fulfillments += 1
                        break

    num_violations = num_activations - num_fulfillments
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations > 0:
        state = TraceState.VIOLATED
    elif done and num_violations == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=None,
                         num_activations=num_activations, state=state)


# mp-alternate-precedence constraint checker
# Description:
# The history-based constraint alternatePrecedence(a, b) indicates that
# each time event b occurs in the trace
# it is preceded by event a and no other event b can recur in between.
# Event b activates the constraint.
def mp_alternate_precedence(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    num_activations = 0
    num_fulfillments = 0
    Ts = []

    for event in trace:
        if event["concept:name"] == a:
            Ts.append(event)

        if event["concept:name"] == b:
            locl = {'A': event}
            if eval(activation_rules, glob, locl):
                num_activations += 1
                for T in Ts:
                    locl = {'A': event, 'T': T, 'timedelta': timedelta, 'abs': abs, 'float': float}
                    if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                        num_fulfillments += 1
                        break
                Ts = []

    num_violations = num_activations - num_fulfillments
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations > 0:
        state = TraceState.VIOLATED
    elif done and num_violations == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=None,
                         num_activations=num_activations, state=state)


# mp-chain-precedence constraint checker
# Description:
# The history-based constraint chain_precedence(a, b) indicates that,
# each time event b occurs in the trace, event a occurs immediately beforehand.
# Event b activates the constraint.
def mp_chain_precedence(trace, done, a, b, rules):
    activation_rules = parse_data_cond(rules["activation"])
    correlation_rules = parse_data_cond(rules["correlation"])
    time_rule = parse_time_cond(rules["time"])

    num_activations = 0
    num_fulfillments = 0

    for index, event in enumerate(trace):
        if event["concept:name"] == b:
            locl = {'A': event}

            if eval(activation_rules, glob, locl):
                num_activations += 1

                if index != 0 and trace[index-1]["concept:name"] == a:
                    locl = {'A': event, 'T': trace[index-1], 'timedelta': timedelta, 'abs': abs, 'float': float}
                    if eval(correlation_rules, glob, locl) and eval(time_rule, glob, locl):
                        num_fulfillments += 1

    num_violations = num_activations - num_fulfillments
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    state = None

    if not vacuous_satisfaction and num_activations == 0:
        if done:
            state = TraceState.VIOLATED
        else:
            state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations > 0:
        state = TraceState.VIOLATED
    elif done and num_violations == 0:
        state = TraceState.SATISFIED

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=None,
                         num_activations=num_activations, state=state)
