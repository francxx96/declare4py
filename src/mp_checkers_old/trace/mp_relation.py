from src.enums import TraceState
from src.models import TraceResult


# mp-responded-existence constraint checker
# Description:
# The future constraining and history-based constraint
# respondedExistence(a, b) indicates that, if event a occurs in the trace
# then event b occurs in the trace as well.
# Event a activates the constraint.
def mp_responded_existence_checker(trace, done, a, b, activation_rules, correlation_rules):
    pendings = []
    ret = True
    num_fulfillments_in_trace = 0
    num_violations_in_trace = 0
    num_pendings_in_trace = 0
    for event in trace:
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                pendings.append(event)
    for event in trace:
        if len(pendings) == 0:
            break
        if event["concept:name"] == b:
            T = event
            for A in reversed(pendings):
                if eval(correlation_rules):
                    pendings.remove(A)
                    num_fulfillments_in_trace += 1
    if done:
        num_violations_in_trace = len(pendings)
    else:
        num_pendings_in_trace = len(pendings)
    num_activations_in_trace = num_fulfillments_in_trace + num_violations_in_trace + num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif done and num_violations_in_trace > 0:
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = num_pendings_in_trace,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-response constraint checker
# Description:
# The future constraining constraint response(a, b) indicates that
# if event a occurs in the trace, then event b occurs after a.
# Event a activates the constraint.
def mp_response_checker(trace, done, a, b, activation_rules, correlation_rules):
    pendings = []
    ret = True
    num_fulfillments_in_trace = 0
    num_violations_in_trace = 0
    num_pendings_in_trace = 0
    for event in trace:
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                pendings.append(event)
        if len(pendings) > 0 and event["concept:name"] == b:
            T = event
            for A in reversed(pendings):
                if eval(correlation_rules):
                    pendings.remove(A)
                    num_fulfillments_in_trace += 1
    if done:
        num_violations_in_trace = len(pendings)
    else:
        num_pendings_in_trace = len(pendings)
    num_activations_in_trace = num_fulfillments_in_trace + num_violations_in_trace + num_pendings_in_trace

    state = None
    if not done and num_pendings_in_trace > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_pendings_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif done and num_violations_in_trace > 0:
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = num_pendings_in_trace,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-alternate-response constraint checker
# Description:
# The future constraining constraint alternateResponse(a, b) indicates that
# each time event a occurs in the trace then event b occurs afterwards
# before event a recurs.
# Event a activates the constraint.
def mp_alternate_response_checker(trace, done, a, b, activation_rules, correlation_rules):
    pending = None
    ret = True
    num_activations_in_trace = 0
    num_fulfillments_in_trace = 0
    num_pendings_in_trace = 0
    for event in trace:
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                pending = event
                num_activations_in_trace += 1
        if event["concept:name"] == b and pending != None:
            A = pending
            T = event
            if eval(correlation_rules):
                pending = None
                num_fulfillments_in_trace += 1
    if not done and pending != None:
        num_pendings_in_trace = 1
    num_violations_in_trace = num_activations_in_trace - num_fulfillments_in_trace - num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace == 0 and num_pendings_in_trace > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations_in_trace == 0 and num_pendings_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0  or (done and num_pendings_in_trace > 0):
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0 and num_pendings_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = num_pendings_in_trace,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-chain-response constraint checker
# Description:
# The future constraining constraint chain_response(a, b) indicates that,
# each time event a occurs in the trace, event b occurs immediately afterwards.
# Event a activates the constraint.
def mp_chain_response_checker(trace, done, a, b, activation_rules, correlation_rules):
    num_activations_in_trace = 0
    ret = True
    num_fulfillments_in_trace = 0
    num_pendings_in_trace = 0
    for index, event in enumerate(trace):
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                num_activations_in_trace += 1
                if index < len(trace) - 1:
                    if trace[index + 1]["concept:name"] == b:
                        T = trace[index + 1]
                        if eval(correlation_rules):
                            num_fulfillments_in_trace += 1
                else:
                    if not done:
                        num_pendings_in_trace = 1
    num_violations_in_trace = num_activations_in_trace - num_fulfillments_in_trace - num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace == 0 and num_pendings_in_trace > 0:
        state = TraceState.POSSIBLY_VIOLATED
    elif not done and num_violations_in_trace == 0 and num_pendings_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0  or (done and num_pendings_in_trace > 0):
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0 and num_pendings_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = num_pendings_in_trace,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-precedence constraint checker
# Description:
# The history-based constraint precedence(a,b) indicates that event b occurs
# only in the trace, if preceded by a. Event b activates the constraint.
# Event b activates the constraint.
def mp_precedence_checker(trace, done, a, b, activation_rules, correlation_rules):
    num_activations_in_trace = 0
    ret = True
    num_fulfillments_in_trace = 0
    Ts = []
    for event in trace:
        if event["concept:name"] == a:
            Ts.append(event)
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations_in_trace += 1
                for T in Ts:
                    if eval(correlation_rules):
                        num_fulfillments_in_trace += 1
                        break
    num_violations_in_trace = num_activations_in_trace - num_fulfillments_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = None,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-alternate-precedence constraint checker
# Description:
# The history-based constraint alternatePrecedence(a, b) indicates that
# each time event b occurs in the trace
# it is preceded by event a and no other event b can recur in between.
# Event b activates the constraint.
def mp_alternate_precedence_checker(trace, done, a, b, activation_rules, correlation_rules):
    num_activations_in_trace = 0
    ret = True
    num_fulfillments_in_trace = 0
    Ts = []
    for event in trace:
        if event["concept:name"] == a:
            Ts.append(event)
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations_in_trace += 1
                for T in Ts:
                    if eval(correlation_rules):
                        num_fulfillments_in_trace += 1
                        break
                Ts = []
    num_violations_in_trace = num_activations_in_trace - num_fulfillments_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = None,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret


# mp-chain-precedence constraint checker
# Description:
# The history-based constraint chain_precedence(a, b) indicates that,
# each time event b occurs in the trace, event a occurs immediately beforehand.
# Event b activates the constraint.
def mp_chain_precedence_checker(trace, done, a, b, activation_rules, correlation_rules):
    num_activations_in_trace = 0
    ret = True
    num_fulfillments_in_trace = 0
    for index, event in enumerate(trace):
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations_in_trace += 1
                if index != 0 and trace[index - 1]["concept:name"] == a:
                    T = trace[index - 1]
                    if eval(correlation_rules):
                        num_fulfillments_in_trace += 1
    num_violations_in_trace = num_activations_in_trace - num_fulfillments_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        state = TraceState.VIOLATED
        ret = False
    elif done and num_violations_in_trace == 0:
        state = TraceState.SATISFIED
        ret = True

    result = TraceResult(
        num_fulfillments_in_trace = num_fulfillments_in_trace,
        num_violations_in_trace = num_violations_in_trace,
        num_pendings_in_trace = None,
        num_activations_in_trace = num_activations_in_trace,
        state = state
    )
    return ret
