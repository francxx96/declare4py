from src.parsers import *
from src.api import *
from src.enums import TraceState

import pm4py
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth


class Declare4Py:
    """
    Class for Declare4Py
    """

    def __init__(self):
        self.log = None
        self.model = None
        self.log_length = None
        self.supported_templates = tuple(map(lambda c: c.value, Template))
        self.binary_encoded_log = None
        self.frequent_item_sets = None
        self.conformance_checking_results = None
        self.query_checking_results = None
        self.discovery_results = None

    def parse_xes_log(self, log_path):
        self.log = pm4py.read_xes(log_path)
        self.log_length = len(self.log)

    def activities_log_projection(self):
        projection = []
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        for trace in self.log:
            tmp_trace = []
            for event in trace:
                tmp_trace.append(event["concept:name"])
            projection.append(tmp_trace)
        return projection

    def resources_log_projection(self):
        projection = []
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        for trace in self.log:
            tmp_trace = []
            for event in trace:
                tmp_trace.append(event["org:group"])
            projection.append(tmp_trace)
        return projection

    def parse_decl_model(self, model_path):
        self.model = parse_decl_from_file(model_path)

    def conformance_checking(self, consider_vacuity: bool):
        if self.log is None:
            raise RuntimeError("You must load the log before checking the model.")
        if self.model is None:
            raise RuntimeError("You must load the DECLARE model before checking the model.")

        self.conformance_checking_results = {}
        for i, trace in enumerate(self.log):
            trc_res = check_trace_conformance(trace, self.model, consider_vacuity)
            self.conformance_checking_results[(i, trace.attributes["concept:name"])] = trc_res

        return self.conformance_checking_results

    def compute_frequent_itemsets(self, min_support: float):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")

        te = TransactionEncoder()
        dataset = self.activities_log_projection()
        te_ary = te.fit(dataset).transform(dataset)
        self.binary_encoded_log = pd.DataFrame(te_ary, columns=te.columns_)

        frequent_itemsets = fpgrowth(self.binary_encoded_log, min_support=min_support, use_colnames=True)
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        self.frequent_item_sets = frequent_itemsets[(frequent_itemsets['length'] <= 2)]

    def discovery(self, consider_vacuity: bool, max_declare_cardinality: int = 3, output_path=None):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must run apriori algorithm before.")
        if max_declare_cardinality <= 0:
            raise RuntimeError("Cardinality must be greater than 0.")

        # Constraint generation from itemsets and DECLARE templates
        unary_list_with_card = (Template.EXISTENCE, Template.ABSENCE, Template.EXACTLY)
        unary_list = [Template.INIT]
        binary_list = (Template.CHOICE, Template.EXCLUSIVE_CHOICE, Template.RESPONDED_EXISTENCE, Template.RESPONSE,
                       Template.ALTERNATE_RESPONSE, Template.CHAIN_RESPONSE, Template.PRECEDENCE,
                       Template.ALTERNATE_PRECEDENCE, Template.CHAIN_PRECEDENCE, Template.NOT_RESPONDED_EXISTENCE,
                       Template.NOT_RESPONSE, Template.NOT_CHAIN_RESPONSE, Template.NOT_PRECEDENCE,
                       Template.NOT_CHAIN_PRECEDENCE)

        activities_decl_format = "activity " + "\nactivity ".join(self.get_log_alphabet_activities()) + "\n"
        constraint_str_list = list()

        for item_set in self.frequent_item_sets['itemsets']:
            length = len(item_set)

            if length == 1:
                for templ in unary_list:
                    constraint_str_list.append(templ + '[' + ', '.join(item_set) + '] | |')
                for templ in unary_list_with_card:
                    for i in range(max_declare_cardinality):
                        constraint_str_list.append(templ + str(i+1) + '[' + ', '.join(item_set) + '] | |')

            elif length == 2:
                for templ in binary_list:
                    constraint_str_list.append(templ + '[' + ', '.join(item_set) + '] | | |')
                    constraint_str_list.append(templ + '[' + ', '.join(reversed(list(item_set))) + '] | | |')

        # Check the constraints for each trace
        self.discovery_results = {}
        for constraint_str in constraint_str_list:
            tmp_decl_model = activities_decl_format + constraint_str

            for i, trace in enumerate(self.log):
                trc_res = check_trace_conformance(trace, parse_decl_from_string(tmp_decl_model), consider_vacuity)

                if trc_res[constraint_str].state == TraceState.SATISFIED:
                    new_val = {(i, trace.attributes['concept:name']): trc_res[constraint_str]}
                    if constraint_str in self.discovery_results:
                        self.discovery_results[constraint_str] |= new_val
                    else:
                        self.discovery_results[constraint_str] = new_val

        if output_path is not None:
            with open(output_path, 'a') as f:
                f.write(activities_decl_format)
                f.write('\n'.join(self.discovery_results.keys()))

        return self.discovery_results

    def filter_discovery(self, min_support: float = 0, output_path=None):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.discovery_results is None:
            raise RuntimeError("You must run a Discovery task before.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")

        result = {}

        for key, val in self.discovery_results.items():
            support = len(val) / len(self.log)
            if support >= min_support:
                result[key] = support

        if output_path is not None:
            with open(output_path, 'a') as f:
                f.write("activity " + "\nactivity ".join(self.get_log_alphabet_activities()) + "\n")
                f.write('\n'.join(result.keys()))

        return result

    def query_checking(self):
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
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        trace_ids = []
        for trace_id, trace in enumerate(self.log):
            trace_ids.append((trace_id, trace.attributes["concept:name"]))
        return trace_ids

    def get_log_length(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        return self.log_length

    def get_log(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        return self.log

    def get_log_alphabet_payload(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        resources = set()
        for trace in self.log:
            for event in trace:
                resources.add(event["org:group"])
        return resources

    def get_log_alphabet_activities(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        activities = set()
        for trace in self.log:
            for event in trace:
                activities.add(event["concept:name"])
        return list(activities)

    def get_frequent_item_sets(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")

        return self.frequent_item_sets

    def get_binary_encoded_log(self):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must run apriori algorithm before.")

        return self.binary_encoded_log
