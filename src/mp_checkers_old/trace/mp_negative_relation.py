from src.enums import TraceState
from src.models import TraceResult


# mp-not-responded-existence constraint checker
# Description:
def mp_not_responded_existence_checker(trace, done, a, b, activation_rules, correlation_rules):
    print("========== mp-responded-existence constraint checker ==========")
    print("inputs: ")
    print("done: ", done)
    print("a: ", a)
    print("b: ", b)
    print("activation rules: ", activation_rules)
    print("correlation rules: ", correlation_rules)
    print("output: ", end="")
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
                    num_violations_in_trace += 1
    if done:
        num_fulfillments_in_trace = len(pendings)
    else:
        num_pendings_in_trace = len(pendings)
    num_activations_in_trace = num_fulfillments_in_trace + num_violations_in_trace + num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        ret = False
        state = TraceState.VIOLATED
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
    print(result.__dict__)
    return ret


# mp-not-response constraint checker
# Description:
def mp_not_response_checker(trace, done, a, b, activation_rules, correlation_rules):
    print("========== mp-response constraint checker ==========")
    print("inputs: ")
    print("done: ", done)
    print("a: ", a)
    print("b: ", b)
    print("activation rules: ", activation_rules)
    print("correlation rules: ", correlation_rules)
    print("output: ", end="")
    ret = True
    pendings = []
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
                    num_violations_in_trace += 1
    if done:
        num_fulfillments_in_trace = len(pendings)
    else:
        num_pendings_in_trace = len(pendings)
    num_activations_in_trace = num_fulfillments_in_trace + num_violations_in_trace + num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        ret = False
        state = TraceState.VIOLATED
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
    print(result.__dict__)
    return ret


# mp-not-chain-response constraint checker
# Description:
def mp_not_chain_response_checker(trace, done, a, b, activation_rules, correlation_rules):
    print("========== mp-not-chain-response constraint checker ==========")
    print("inputs: ")
    print("done: ", done)
    print("a: ", a)
    print("b: ", b)
    print("activation rules: ", activation_rules)
    print("correlation rules: ", correlation_rules)
    print("output: ", end="")
    ret = True
    num_activations_in_trace = 0
    num_violations_in_trace = 0
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
                            num_violations_in_trace += 1
                else:
                    if not done:
                        num_pendings_in_trace = 1
    num_fulfillments_in_trace = num_activations_in_trace - num_violations_in_trace - num_pendings_in_trace

    state = None
    if not done and num_violations_in_trace == 0:
        state = TraceState.POSSIBLY_SATISFIED
    elif num_violations_in_trace > 0:
        ret = False
        state = TraceState.VIOLATED
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
    print(result.__dict__)
    return ret


# mp-not-precedence constraint checker
# Description:
def mp_not_precedence_checker(trace, done, a, b, activation_rules, correlation_rules):
    print("========== mp-not-precedence constraint checker ==========")
    print("inputs: ")
    print("done: ", done)
    print("a: ", a)
    print("b: ", b)
    print("activation rules: ", activation_rules)
    print("correlation rules: ", correlation_rules)
    print("output: ", end="")
    ret = True
    num_activations_in_trace = 0
    num_violations_in_trace = 0
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
                        num_violations_in_trace += 1
                        break
    num_fulfillments_in_trace = num_activations_in_trace - num_violations_in_trace

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
    print(result.__dict__)
    return ret


# mp-not-chain-precedence constraint checker
# Description:
def mp_not_chain_precedence_checker(trace, done, a, b, activation_rules, correlation_rules):
    print("========== mp-not-chain-precedence constraint checker ==========")
    print("inputs: ")
    print("done: ", done)
    print("a: ", a)
    print("b: ", b)
    print("activation rules: ", activation_rules)
    print("correlation rules: ", correlation_rules)
    print("output: ", end="")
    ret = True
    num_activations_in_trace = 0
    num_violations_in_trace = 0
    for index, event in enumerate(trace):
        if event["concept:name"] == b:
            A = event
            if eval(activation_rules):
                num_activations_in_trace += 1
                if index != 0 and trace[index - 1]["concept:name"] == a:
                    T = trace[index - 1]
                    if eval(correlation_rules):
                        num_violations_in_trace += 1
    num_fulfillments_in_trace = num_activations_in_trace - num_violations_in_trace

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
