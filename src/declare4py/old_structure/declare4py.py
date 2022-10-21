from src.declare4py.old_structure.decl_parser import *
from src.declare4py.old_structure.api_functions import *
import sys
from itertools import product


class Declare4Py:

    """
    Wrapper that collects the input log and model, the supported templates, the output for the discovery, conformance
    checking and query checking tasks. In addition, it contains the computed binary encoding and frequent item sets
    for the input log.

    Attributes
    ----------
    log : EventLog
        the input event log parsed from a XES file
    model : DeclModel
        the input DECLARE model parsed from a decl file
    log_length : int
        the trace number of the input log
    supported_templates : tuple[str]
        tuple containing all the DECLARE templates supported by the Declare4Py library
    binary_encoded_log : DataFrame
        the binary encoded version of the input log
    frequent_item_sets : DataFrame
        list of the most frequent item sets found along the log traces, together with their support and length
    conformance_checking_results : dict[tuple[int, str]: dict[str: CheckerResult]]
        output dictionary of the conformance_checking() function. Each entry contains:
        key = tuple[trace_pos_inside_log, trace_name]
        val = dict[ constraint_string : CheckerResult ]
    query_checking_results : dict[str: dict[str: str]]
        output dictionary of the query_checking() function. Each entry contains:
        key = constraint_string
        val = dict[ constraint_elem_key : constraint_elem_val ]
    discovery_results : dict[str: dict[tuple[int, str]: CheckerResult]]
        output dictionary of the discovery() function. Each entry contains:
        key = constraint_string
        val = dict[ tuple[trace_pos_inside_log, trace_name] : CheckerResult ]
    """
    def __init__(self):
        self.log = None
        self.model = None
        self.log_length = None
        self.supported_templates = tuple(map(lambda c: c.templ_str, Template))
        self.binary_encoded_log = None
        self.frequent_item_sets = None
        self.conformance_checking_results = None
        self.query_checking_results = None
        self.discovery_results = None


    # DECLARE UTILITIES
    def parse_decl_model(self, model_path) -> None:
        """
        Parse the input DECLARE model.

        Parameters
        ----------
        model_path : str
            File path where the DECLARE model is stored.
        """
        self.model = parse_decl_from_file(model_path)

    def get_supported_templates(self) -> tuple[str, ...]:
        """
        Return the DECLARE templates supported by Declare4Py.

        Returns
        -------
        supported_templates
            tuple of names of the supported DECLARE templates.
        """
        return self.supported_templates



    # FUNCTIONS FOR PRINTING RESULTS ##############
    def print_conformance_results(self):
        if self.conformance_checking_results is None:
            raise RuntimeError("You must run conformance checking before!")

        for key, value in self.conformance_checking_results.items():
            print('Trace ID: ' + str(key[0]) + ' - "' + key[1] + '"')
            for item in value.items():
                print('\t' + item[1].state + '\ton ' + item[0])
            print()
