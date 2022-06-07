from src.enums import TraceState
from src.models import CheckerResult
from datetime import timedelta


# mp-not-responded-existence constraint checker
# Description:
def mp_not_responded_existence(trace, done, a, b, rules):
    activation_rules = rules["activation"]
    correlation_rules = rules["correlation"]
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    time_rule = rules["time"]

    pendings = []
    num_fulfillments = 0
    num_violations = 0
    num_pendings = 0
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
                if eval(correlation_rules) and eval(time_rule):
                    pendings.remove(A)
                    num_violations += 1
    if done:
        num_fulfillments = len(pendings)
    else:
        num_pendings = len(pendings)
    num_activations = num_fulfillments + num_violations + num_pendings

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

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings, num_activations=num_activations, state=state)


# mp-not-response constraint checker
# Description:
def mp_not_response(trace, done, a, b, rules):
    activation_rules = rules["activation"]
    correlation_rules = rules["correlation"]
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    time_rule = rules["time"]

    pendings = []
    num_fulfillments = 0
    num_violations = 0
    num_pendings = 0
    for event in trace:
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                pendings.append(event)
        if len(pendings) > 0 and event["concept:name"] == b:
            T = event
            for A in reversed(pendings):
                if eval(correlation_rules) and eval(time_rule):
                    pendings.remove(A)
                    num_violations += 1
    if done:
        num_fulfillments = len(pendings)
    else:
        num_pendings = len(pendings)
    num_activations = num_fulfillments + num_violations + num_pendings

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

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings, num_activations=num_activations, state=state)


# mp-not-chain-response constraint checker
# Description:
def mp_not_chain_response(trace, done, a, b, rules):
    activation_rules = rules["activation"]
    correlation_rules = rules["correlation"]
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    time_rule = rules["time"]

    num_activations = 0
    num_violations = 0
    num_pendings = 0
    for index, event in enumerate(trace):
        if event["concept:name"] == a:
            A = event
            if eval(activation_rules):
                num_activations += 1
                if index < len(trace) - 1:
                    if trace[index + 1]["concept:name"] == b:
                        T = trace[index + 1]
                        if eval(correlation_rules) and eval(time_rule):
                            num_violations += 1
                else:
                    if not done:
                        num_pendings = 1
    num_fulfillments = num_activations - num_violations - num_pendings

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

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=num_pendings, num_activations=num_activations, state=state)


# mp-not-precedence constraint checker
# Description:
def mp_not_precedence(trace, done, a, b, rules):
    activation_rules = rules["activation"]
    correlation_rules = rules["correlation"]
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    time_rule = rules["time"]

    num_activations = 0
    num_violations = 0
    Ts = []
    for event in trace:
        if event["concept:name"] == a:
            Ts.append(event)
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations += 1
                for T in Ts:
                    if eval(correlation_rules) and eval(time_rule):
                        num_violations += 1
                        break
    num_fulfillments = num_activations - num_violations

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

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=None, num_activations=num_activations, state=state)


# mp-not-chain-precedence constraint checker
# Description:
def mp_not_chain_precedence(trace, done, a, b, rules):
    activation_rules = rules["activation"]
    correlation_rules = rules["correlation"]
    vacuous_satisfaction = rules["vacuous_satisfaction"]
    time_rule = rules["time"]

    num_activations = 0
    num_violations = 0
    for index, event in enumerate(trace):
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations += 1
                if index != 0 and trace[index - 1]["concept:name"] == a:
                    T = trace[index - 1]
                    if eval(correlation_rules) and eval(time_rule):
                        num_violations += 1
    num_fulfillments = num_activations - num_violations

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

    return CheckerResult(num_fulfillments=num_fulfillments, num_violations=num_violations, num_pendings=None, num_activations=num_activations, state=state)
