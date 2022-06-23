from src.parsers import *
from src.api import *

import pm4py
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori
from itertools import product


class Declare4Py:
    """
    Class for Declare4Py
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

    # LOG MANAGEMENT UTILITIES
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

    def log_encoding(self, dimension: str = 'act'):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        te = TransactionEncoder()
        if dimension == 'act':
            dataset = self.activities_log_projection()
        elif dimension == 'payload':
            dataset = self.resources_log_projection()
        else:
            raise RuntimeError(f"{dimension} dimension not supported. Choose between act and payload")
        te_ary = te.fit(dataset).transform(dataset)
        self.binary_encoded_log = pd.DataFrame(te_ary, columns=te.columns_)
        return self.binary_encoded_log

    def compute_frequent_itemsets(self, min_support: float, dimension: str = 'act', algorithm: str = 'fpgrowth',
                                  len_itemset: int = None):
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")

        self.log_encoding(dimension)
        if algorithm == 'fpgrowth':
            frequent_itemsets = fpgrowth(self.binary_encoded_log, min_support=min_support, use_colnames=True)
        elif algorithm == 'apriori':
            frequent_itemsets = apriori(self.binary_encoded_log, min_support=min_support, use_colnames=True)
        else:
            raise RuntimeError(f"{algorithm} algorithm not supported. Choose between fpgrowth and apriori")
        frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
        if len_itemset is None:
            self.frequent_item_sets = frequent_itemsets
        else:
            self.frequent_item_sets = frequent_itemsets[(frequent_itemsets['length'] <= len_itemset)]

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

    # DECLARE UTILITIES
    def parse_decl_model(self, model_path):
        self.model = parse_decl_from_file(model_path)

    def get_supported_templates(self):
        return self.supported_templates

    def get_model_activities(self):
        return self.model.activities

    def get_model_constraints(self):
        return self.model.get_decl_model_constraints()

    # PROCESS MINING TASKS
    def conformance_checking(self, consider_vacuity: bool):
        print("Computing conformance checking ...")
        if self.log is None:
            raise RuntimeError("You must load the log before checking the model.")
        if self.model is None:
            raise RuntimeError("You must load the DECLARE model before checking the model.")

        self.conformance_checking_results = {}
        for i, trace in enumerate(self.log):
            trc_res = check_trace_conformance(trace, self.model, consider_vacuity)
            self.conformance_checking_results[(i, trace.attributes["concept:name"])] = trc_res

        return self.conformance_checking_results

    def discovery(self, consider_vacuity: bool, max_declare_cardinality: int = 3, output_path=None):
        print("Computing discovery ...")
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must discover frequent itemsets before.")
        if max_declare_cardinality <= 0:
            raise RuntimeError("Cardinality must be greater than 0.")

        self.discovery_results = {}

        for item_set in self.frequent_item_sets['itemsets']:
            length = len(item_set)

            if length == 1:
                for templ in Template.get_unary_templates():
                    constraint = {"template": templ, "attributes": ', '.join(item_set), "condition": ("", "")}
                    if not templ.supports_cardinality:
                        self.discovery_results |= discover_constraint(self.log, constraint, consider_vacuity)
                    else:
                        for i in range(max_declare_cardinality):
                            constraint['n'] = i+1
                            self.discovery_results |= discover_constraint(self.log, constraint, consider_vacuity)

            elif length == 2:
                for templ in Template.get_binary_templates():
                    constraint = {"template": templ, "attributes": ', '.join(item_set), "condition": ("", "", "")}
                    self.discovery_results |= discover_constraint(self.log, constraint, consider_vacuity)

                    constraint['attributes'] = ', '.join(reversed(list(item_set)))
                    self.discovery_results |= discover_constraint(self.log, constraint, consider_vacuity)

        activities_decl_format = "activity " + "\nactivity ".join(self.get_log_alphabet_activities()) + "\n"
        if output_path is not None:
            with open(output_path, 'w') as f:
                f.write(activities_decl_format)
                f.write('\n'.join(self.discovery_results.keys()))

        return self.discovery_results

    def filter_discovery(self, min_support: float = 0, output_path: str = None):
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
            with open(output_path, 'w') as f:
                f.write("activity " + "\nactivity ".join(self.get_log_alphabet_activities()) + "\n")
                f.write('\n'.join(result.keys()))

        return result

    def query_checking(self, consider_vacuity: bool, template_str: str = None, max_declare_cardinality: int = 1,
                       activation: str = None, target: str = None, act_cond: str = "", trg_cond: str = "",
                       time_cond: str = "", min_support: float = 0.0, return_first: bool = False):
        print("Computing query checking ...")
        if template_str is None and activation is None and target is None:
            raise RuntimeError("You must set at least one parameter among (template, activation, target).")
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")
        if max_declare_cardinality <= 0:
            raise RuntimeError("Cardinality must be greater than 0.")

        templates_to_check = list()
        cardinality = None
        if template_str is None:
            templates_to_check = list(Template)
        else:
            template_search = re.search(r'(^\D+)(\d*$)', template_str)
            if template_search is not None:
                template_str, cardinality = template_search.groups()
                template = Template.get_template_from_string(template_str)
                if template is not None:
                    templates_to_check.append(template)
                else:
                    raise RuntimeError("You must insert a supported DECLARE template.")
            else:
                raise RuntimeError("You must insert a supported DECLARE template.")

        activations_to_check = self.get_log_alphabet_activities() if activation is None else [activation]
        targets_to_check = self.get_log_alphabet_activities() if target is None else [target]
        activity_combos = filter(lambda comb: comb[0] != comb[1], product(activations_to_check, targets_to_check))

        self.query_checking_results = {}

        for template in templates_to_check:
            constraint = {"template": template}
            res_value = {"template": template.templ_str}

            if template.is_binary:
                constraint['condition'] = (act_cond, trg_cond, time_cond)
                res_value |= {"act_cond": act_cond, "trg_cond": trg_cond, "time_cond": time_cond}

                for couple in activity_combos:
                    constraint['attributes'] = ', '.join(couple)
                    res_value |= {"activation": couple[0], "target": couple[1]}

                    if template.supports_cardinality:
                        if cardinality is not None:
                            constraint['n'] = int(cardinality)
                            res_value['template'] += cardinality
                            for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                                if len(res) / len(self.log) >= min_support:
                                    self.query_checking_results[constraint_str] = res_value
                                    if return_first:
                                        return self.query_checking_results
                        else:
                            for i in range(max_declare_cardinality):
                                constraint['n'] = i+1
                                res_value['template'] += str(i+1)
                                for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                                    if len(res) / len(self.log) >= min_support:
                                        self.query_checking_results[constraint_str] = res_value
                                        if return_first:
                                            return self.query_checking_results
                    else:
                        for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                            if len(res) / len(self.log) >= min_support:
                                self.query_checking_results[constraint_str] = res_value
                                if return_first:
                                    return self.query_checking_results

            else:   # unary constraint
                constraint['condition'] = (act_cond, time_cond)
                res_value |= {"act_cond": act_cond, "time_cond": time_cond}

                for activity in activations_to_check:
                    constraint['attributes'] = activity
                    res_value |= {"activation": activity}

                    if template.supports_cardinality:
                        if cardinality is not None:
                            constraint['n'] = int(cardinality)
                            res_value['template'] += cardinality
                            for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                                if len(res) / len(self.log) >= min_support:
                                    self.query_checking_results[constraint_str] = res_value
                                    if return_first:
                                        return self.query_checking_results
                        else:
                            for i in range(max_declare_cardinality):
                                constraint['n'] = i+1
                                res_value['template'] += str(i+1)
                                for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                                    if len(res) / len(self.log) >= min_support:
                                        self.query_checking_results[constraint_str] = res_value
                                        if return_first:
                                            return self.query_checking_results
                    else:
                        for constraint_str, res in discover_constraint(self.log, constraint, consider_vacuity).items():
                            if len(res) / len(self.log) >= min_support:
                                self.query_checking_results[constraint_str] = res_value
                                if return_first:
                                    return self.query_checking_results

        return self.query_checking_results

    # FUNCTIONS FOR PRINTING RESULTS ##############
    def print_conformance_results(self):
        if self.conformance_checking_results is None:
            raise RuntimeError("You must run conformance checking before!")

        for key, value in self.conformance_checking_results.items():
            print('Trace ID: ' + str(key[0]) + ' - "' + key[1] + '"')
            for item in value.items():
                print('\t' + item[1].state + '\ton ' + item[0])
            print()
