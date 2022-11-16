from declare4py.src.declare4py.models.basic_mp_declare_conformance_checking import BasicMPDeclareConformanceChecking

"""
Initializes class ConformanceCheckingResults

Attributes
-------
    dict_results : dict
        dictionary of conformance checking results

"""


class ConformanceCheckingResults:

    def __init__(self, dict_results: dict):
        self.dict_results: dict = dict_results
        BasicMPDeclareConformanceChecking.__init__(self)
