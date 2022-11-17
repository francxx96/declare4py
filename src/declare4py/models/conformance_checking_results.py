
"""
Initializes class ConformanceCheckingResults

Attributes
-------
    dict_results : dict
        dictionary of conformance checking results

    BasicMPDeclareConformanceChecking
        inherit class init
"""
from src.declare4py.models.basic_mp_declare_conformance_checking import BasicMPDeclareConformanceChecking


class ConformanceCheckingResults:

    def __init__(self, dict_results: dict):
        self.dict_results: dict = dict_results
        BasicMPDeclareConformanceChecking.__init__(self)
