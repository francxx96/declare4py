from src.parsers import *
from src.api import *
import pm4py
import pdb

class Declare4Py:
    """
    Class for Declare4Py
    """
    def __init__(self):
        self.log = None
        self.model = None
        self.log_length = None
        self.supported_templates = tuple(map(lambda c: c.value, Template))
        self.frequent_item_sets = None
        self.conformance_checking_results = None
        self.query_checking_results = None
        self.discovery_results = None

    def parse_xes_log(self, log_path):
        self.log = pm4py.read_xes(log_path)
        self.log_length = len(self.log)

    def parse_decl_model(self, model_path):
        self.model = parse_decl(model_path)

    def conformance_checking(self, consider_vacuity):
        if self.log is None:
            raise RuntimeError("You must load the log before checking the model!")
        if self.model is None:
            raise RuntimeError("You must load the DECLARE model before checking the model!")

        self.conformance_checking_results = conformance_checking(self.log, self.model, consider_vacuity)
        return self.conformance_checking_results

    def run_apriori(self, support=0):
        self.frequent_item_sets = {}

    def query_checking(self):
        pass

    def discovery(self):
        pass

    def filter_discovery(self, support):
        pass

    # FUNCTIONS FOR PRINTING RESULTS ##############

    def print_conformance_results(self):
        if self.conformance_checking_results is None:
            raise RuntimeError("You must run conformance checking before!")

        for key, value in self.conformance_checking_results.items():
            print('Trace ID: ' + str(key[0]) + ' - "' + key[1] + '"')
            for item in value.items():
                print('\t' + item[1].state + '\ton ' + item[0])
            print()

    def get_supported_templates(self):
        return self.supported_templates

    def get_model_activities(self):
        return self.model.activities

    def get_model_constraints(self):
        return self.model.get_decl_model_constraints()
    
    def get_trace_keys(self):
        trace_ids = []
        for trace_id, trace in enumerate(self.log):
            trace_ids.append((trace_id, trace.attributes["concept:name"]))
        return trace_ids

    def get_log_length(self):
        return self.log_length

    def get_log(self):
        return self.log
    
    def get_log_payload(self):
        resources = set()
        for trace in self.log:
            for event in trace:
                resources.add(event["org:group"])
        return resources

    def get_log_activities(self):
        activities = set()
        for trace in self.log:
            for event in trace:
                activities.add(event["concept:name"])
        return list(activities)
