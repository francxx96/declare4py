from _future_ import annotations

"""
Initializes class ConformanceCheckingResults

Attributes
-------
    dict_results : dict
        dictionary of conformance checking results
"""


class BasicConformanceCheckingResults:

    def __init__(self, dict_results: dict):
        self.basic_conformance_checking_results: dict = dict_results

    def pendings(self, trace_id: int, constr_id: int) -> int:
        if trace_id == None and constr_id == None:
            print("ERROR: at least one parameter is expected.")
        elif trace_id == None:
            # TODO: returns a dictionary with all the traces in model respecting the specified constraint
            # TODO: count the elements in dictionary and return that number
            pass
        elif constr_id == None:
            # TODO: returns a dictionary with all the constraints in model for the specified trace
            # TODO: count the elements in dictionary and return that number
            pass

    def activations(self, trace_id: int, constr_id: int) -> int:
        if trace_id == None and constr_id == None:
            print("ERROR: at least one parameter is expected.")
        elif trace_id == None:
            # TODO: returns a dictionary with all the traces in model respecting the specified constraint
            # TODO: count the elements in dictionary and return that number
            pass
        elif constr_id == None:
            # TODO: returns a dictionary with all the constraints in model for the specified trace
            # TODO: count the elements in dictionary and return that number
            pass

    def violations(self, trace_id: int, constr_id: int) -> int:
        if trace_id == None and constr_id == None:
            print("ERROR: at least one parameter is expected.")
        elif trace_id == None:
            # TODO: returns a dictionary with all the traces in model respecting the specified constraint
            # TODO: count the elements in dictionary and return that number
            pass
        elif constr_id == None:
            # TODO: returns a dictionary with all the constraints in model for the specified trace
            # TODO: count the elements in dictionary and return that number
            pass

    def fullfillments(self, trace_id: int, constr_id: int) -> int:
        if trace_id == None and constr_id == None:
            print("ERROR: at least one parameter is expected.")
        elif trace_id == None:
            # TODO: returns a dictionary with all the traces in model respecting the specified constraint
            # TODO: count the elements in dictionary and return that number
            pass
        elif constr_id == None:
            # TODO: returns a dictionary with all the constraints in model for the specified trace
            # TODO: count the elements in dictionary and return that number
            pass

    def state(self, trace_id: int, constr_id: int) -> bool:
        if trace_id == None and constr_id == None:
            print("ERROR: at least one parameter is expected.")
        elif trace_id == None:
            # TODO: returns a dictionary with all the traces in model respecting the specified constraint
            # TODO: count the elements in dictionary and return that number
            pass
        elif constr_id == None:
            # TODO: returns a dictionary with all the constraints in model for the specified trace
            # TODO: count the elements in dictionary and return that number
            pass

    def clean(self):
        return self.basic_conformance_checking_results