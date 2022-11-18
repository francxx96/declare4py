from abc import ABC

from src.declare4py.api_functions import check_trace_conformance
from src.declare4py.core.conf_checking import ConformanceChecking
from src.declare4py.models.conformance_checking_results import BasicConformanceCheckingResults

"""
Provides basic conformance checking functionalities

Parameters
--------
    conformance_checking_results : dict
        return type for this class
        
    ConformanceChecking
        inheriting init function
"""


class BasicMPDeclareConformanceChecking(ConformanceChecking, ABC):

    def __init__(self, consider_vacuity):
        self.conformance_checking_results = None
        super().__init__(consider_vacuity)

    def run(self, consider_vacuity: bool) -> BasicConformanceCheckingResults:
        """
        Performs conformance checking for the provided event log and DECLARE model.

        Parameters
        ----------
        consider_vacuity : bool
            True means that vacuously satisfied traces are considered as satisfied, violated otherwise.

        Returns
        -------
        conformance_checking_results
            dictionary where the key is a list containing trace position inside the log and the trace name, the value is
            a dictionary with keys the names of the constraints and values a CheckerResult object containing
            the number of pendings, activations, violations, fulfilments and the truth value of the trace for that
            constraint.
        """
        print("Computing conformance checking ...")
        if self.log is None:
            raise RuntimeError("You must load the log before checking the model.")
        if self.model is None:
            raise RuntimeError("You must load the DECLARE model before checking the model.")

        self.conformance_checking_results = ConformanceCheckingResults({})
        for i, trace in enumerate(self.log):
            trc_res = check_trace_conformance(trace, self.model, consider_vacuity)
            self.conformance_checking_results[(i, trace.attributes["concept:name"])] = trc_res

        return self.conformance_checking_results
