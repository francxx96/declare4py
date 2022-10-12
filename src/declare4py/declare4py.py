from .parsers import *
from .api_functions import *
import sys
import pm4py
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, apriori
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
        self.log_length = None # exported to log utils
        self.supported_templates = tuple(map(lambda c: c.templ_str, Template))
        self.binary_encoded_log = None # exported to log utils
        self.frequent_item_sets = None # exported to log utils
        self.conformance_checking_results = None
        self.query_checking_results = None
        self.discovery_results = None

    # LOG MANAGEMENT UTILITIES
    # exported to log utils
    def get_binary_encoded_log(self) -> pd.DataFrame:
        """
        Return the one-hot encoding of the log.

        Returns
        -------
        binary_encoded_log
            the one-hot encoded log.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must run the item set extraction algorithm before.")

        return self.binary_encoded_log

    # exported to log utils
    def parse_xes_log(self, log_path: str) -> None:
        """
        Set the 'log' EventLog object and the 'log_length' integer by reading and parsing the log corresponding to
        given log file path.

        Parameters
        ----------
        log_path : str
            File path where the log is stored.
        """
        self.log = pm4py.read_xes(log_path)
        self.log_length = len(self.log)

    # exported to log utils
    def activities_log_projection(self) -> list[list[str]]:
        """
        Return for each trace a time-ordered list of the activity names of the events.

        Returns
        -------
        projection
            nested lists, the outer one addresses traces while the inner one contains event activity names.
        """
        projection = []
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        for trace in self.log:
            tmp_trace = []
            for event in trace:
                tmp_trace.append(event["concept:name"])
            projection.append(tmp_trace)
        return projection

    # exported to log utils
    def resources_log_projection(self) -> list[list[str]]:
        """
        Return for each trace a time-ordered list of the resources of the events.

        Returns
        -------
        projection
            nested lists, the outer one addresses traces while the inner one contains event activity names.
        """
        projection = []
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        for trace in self.log:
            tmp_trace = []
            for event in trace:
                tmp_trace.append(event["org:group"])
            projection.append(tmp_trace)
        return projection

    # exported to log utils
    def log_encoding(self, dimension: str = 'act') -> pd.DataFrame:
        """
        Return the log binary encoding, i.e. the one-hot encoding stating whether an attribute is contained
        or not inside each trace of the log.

        Parameters
        ----------
        dimension : str, optional
            choose 'act' to perform the encoding over activity names, 'payload' over resources (default 'act').

        Returns
        -------
        binary_encoded_log
            the one-hot encoding of the input log, made over activity names or resources depending on 'dimension' value.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        te = TransactionEncoder()
        if dimension == 'act':
            dataset = self.activities_log_projection()
        elif dimension == 'payload':
            dataset = self.resources_log_projection()
        else:
            raise RuntimeError(f"{dimension} dimension not supported. Choose between 'act' and 'payload'")
        te_ary = te.fit(dataset).transform(dataset)
        self.binary_encoded_log = pd.DataFrame(te_ary, columns=te.columns_)
        return self.binary_encoded_log

    # exported to log utils
    def compute_frequent_itemsets(self, min_support: float, dimension: str = 'act', algorithm: str = 'fpgrowth',
                                  len_itemset: int = None) -> None:
        """
        Compute the most frequent item sets with a support greater or equal than 'min_support' with the given algorithm
        and over the given dimension.

        Parameters
        ----------
        min_support: float
            the minimum support of the returned item sets.
        dimension : str, optional
            choose 'act' to perform the encoding over activity names, 'payload' over resources (default 'act').
        algorithm : str, optional
            the algorithm for extracting frequent itemsets, choose between 'fpgrowth' (default) and 'apriori'.
        len_itemset : int, optional
            the maximum length of the extracted itemsets.
        """
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

    def get_trace_keys(self) -> list[tuple[int, str]]:
        """
        Return the name of each trace, along with the position in the log.

        Returns
        -------
        trace_ids
            list containing the position in the log and the name of the trace.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        trace_ids = []
        for trace_id, trace in enumerate(self.log):
            trace_ids.append((trace_id, trace.attributes["concept:name"]))
        return trace_ids

    # exported to log utils
    def get_log_length(self) -> int:
        """
        Return the number of traces contained in the log.

        Returns
        -------
        log_length
            the length of the log.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        return self.log_length

    # exported to log utils
    def get_log(self) -> pm4py.objects.log.obj.EventLog:
        """
        Return the log previously fed in input.

        Returns
        -------
        log
            the input log.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        return self.log

    # exported to log utils
    def get_log_alphabet_payload(self) -> set[str]:
        """
        Return the set of resources that are in the log.

        Returns
        -------
        resources
            resource set.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        resources = set()
        for trace in self.log:
            for event in trace:
                resources.add(event["org:group"])
        return resources

    # exported to log utils
    def get_log_alphabet_activities(self):
        """
        Return the set of activities that are in the log.

        Returns
        -------
        activities
            activity set.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        activities = set()
        for trace in self.log:
            for event in trace:
                activities.add(event["concept:name"])
        return list(activities)

    # exported to log utils
    def get_frequent_item_sets(self) -> pd.DataFrame:
        """
        Return the set of extracted frequent item sets.

        Returns
        -------
        frequent_item_sets
            the set of extracted frequent item sets.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must run the item set extraction algorithm before.")

        return self.frequent_item_sets

    # exported to log utils
    def get_binary_encoded_log(self) -> pd.DataFrame:
        """
        Return the one-hot encoding of the log.

        Returns
        -------
        binary_encoded_log
            the one-hot encoded log.
        """
        if self.log is None:
            raise RuntimeError("You must load a log before.")
        if self.frequent_item_sets is None:
            raise RuntimeError("You must run the item set extraction algorithm before.")

        return self.binary_encoded_log

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

    def get_model_activities(self) -> list[str]:
        """
        Return the activities contained in the DECLARE model.

        Returns
        -------
        activities
            list of activity names contained in the DECLARE model.
        """
        if self.model is None:
            raise RuntimeError("You must load a DECLARE model before.")

        return self.model.activities

    def get_model_constraints(self) -> list[str]:
        """
        Return the constraints contained in the DECLARE model.

        Returns
        -------
        activities
            list of constraints contained in the DECLARE model.
        """
        if self.model is None:
            raise RuntimeError("You must load a DECLARE model before.")

        return self.model.get_decl_model_constraints()

    # PROCESS MINING TASKS
    def conformance_checking(self, consider_vacuity: bool) -> dict[tuple[int, str]: dict[str: CheckerResult]]:
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

        self.conformance_checking_results = {}
        for i, trace in enumerate(self.log):
            trc_res = check_trace_conformance(trace, self.model, consider_vacuity)
            self.conformance_checking_results[(i, trace.attributes["concept:name"])] = trc_res

        return self.conformance_checking_results

    def discovery(self, consider_vacuity: bool, max_declare_cardinality: int = 3, output_path: str = None) \
            -> dict[str: dict[tuple[int, str]: CheckerResult]]:
        """
        Performs discovery of the supported DECLARE templates for the provided log by using the computed frequent item
        sets.

        Parameters
        ----------
        consider_vacuity : bool
            True means that vacuously satisfied traces are considered as satisfied, violated otherwise.

        max_declare_cardinality : int, optional
            the maximum cardinality that the algorithm checks for DECLARE templates supporting it (default 3).

        output_path : str, optional
            if specified, save the discovered constraints in a DECLARE model to the provided path.

        Returns
        -------
        discovery_results
            dictionary containing the results indexed by discovered constraints. The value is a dictionary with keys
            the tuples containing id and name of traces that satisfy the constraint. The values of this inner dictionary
            is a CheckerResult object containing the number of pendings, activations, violations, fulfilments.
        """
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

    def filter_discovery(self, min_support: float = 0, output_path: str = None) \
            -> dict[str: dict[tuple[int, str]: CheckerResult]]:
        """
        Filters discovery results by means of minimum support.

        Parameters
        ----------
        min_support : float, optional
            the minimum support that a discovered constraint needs to have to be included in the filtered result.

        output_path : str, optional
            if specified, save the filtered constraints in a DECLARE model to the provided path.

        Returns
        -------
        result
            dictionary containing the results indexed by discovered constraints. The value is a dictionary with keys
            the tuples containing id and name of traces that satisfy the constraint. The values of this inner dictionary
            is a CheckerResult object containing the number of pendings, activations, violations, fulfilments.
        """
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

    def query_checking(self, consider_vacuity: bool,
                       template_str: str = None, max_declare_cardinality: int = 1,
                       activation: str = None, target: str = None,
                       act_cond: str = None, trg_cond: str = None, time_cond: str = None,
                       min_support: float = 1.0, return_first: bool = False) -> dict[str: dict[str: str]]:
        """
        Performs query checking for a (list of) template, activation activity and target activity. Optional
        activation, target and time conditions can be specified.

        Parameters
        ----------
        consider_vacuity : bool
            True means that vacuously satisfied traces are considered as satisfied, violated otherwise.

        template_str : str, optional
            if specified, the query checking is restricted on this DECLARE template. If not, the query checking is
            performed over the whole set of supported templates.

        max_declare_cardinality : int, optional
            the maximum cardinality that the algorithm checks for DECLARE templates supporting it (default 1).

        activation : str, optional
            if specified, the query checking is restricted on this activation activity. If not, the query checking
            considers in turn each activity of the log as activation.

        target : str, optional
            if specified, the query checking is restricted on this target activity. If not, the query checking
            considers in turn each activity of the log as target.

        act_cond : str, optional
            optional activation condition to evaluate. It has to be written by following the DECLARE standard format.

        trg_cond : str, optional
            optional target condition to evaluate. It has to be written by following the DECLARE standard format.

        time_cond : str, optional
            optional time condition to evaluate. It has to be written by following the DECLARE standard format.

        min_support : float, optional
            the minimum support that a constraint needs to have to be included in the result (default 1).

        return_first : bool, optional
            if True, the algorithm returns only the first queried constraint that is above the minimum support. If
            False, the algorithm returns all the constraints above the min. support (default False).

        Returns
        -------
        query_checking_results
            dictionary with keys the DECLARE constraints satisfying the assignments. The values are a structured
            representations of these constraints.
        """
        print("Computing query checking ...")

        is_template_given = bool(template_str)
        is_activation_given = bool(activation)
        is_target_given = bool(target)
        if not act_cond:
            act_cond = ""
        if not trg_cond:
            trg_cond = ""
        if not time_cond:
            time_cond = ""

        if not is_template_given and not is_activation_given and not is_target_given:
            raise RuntimeError("You must set at least one parameter among (template, activation, target).")
        if is_template_given:
            template = Template.get_template_from_string(template_str)
            if template is None:
                raise RuntimeError("You must insert a supported DECLARE template.")
            if not template.is_binary and is_target_given:
                raise RuntimeError("You cannot specify a target activity for unary templates.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")
        if max_declare_cardinality <= 0:
            raise RuntimeError("Cardinality must be greater than 0.")
        if self.log is None:
            raise RuntimeError("You must load a log before.")

        templates_to_check = list()
        if is_template_given:
            templates_to_check.append(template_str)
        else:
            templates_to_check += list(map(lambda t: t.templ_str, Template.get_binary_templates()))
            if not is_target_given:
                for template in Template.get_unary_templates():
                    if template.supports_cardinality:
                        for card in range(max_declare_cardinality):
                            templates_to_check.append(template.templ_str + str(card+1))
                    else:
                        templates_to_check.append(template.templ_str)

        activations_to_check = self.get_log_alphabet_activities() if activation is None else [activation]
        targets_to_check = self.get_log_alphabet_activities() if target is None else [target]
        activity_combos = tuple(filter(lambda c: c[0] != c[1], product(activations_to_check, targets_to_check)))

        self.query_checking_results = {}

        for template_str in templates_to_check:
            template_str, cardinality = re.search(r'(^.+?)(\d*$)', template_str).groups()
            template = Template.get_template_from_string(template_str)

            constraint = {"template": template}
            if cardinality:
                constraint['n'] = int(cardinality)

            if template.is_binary:
                constraint['condition'] = (act_cond, trg_cond, time_cond)
                for couple in activity_combos:
                    constraint['attributes'] = ', '.join(couple)

                    constraint_str = query_constraint(self.log, constraint, consider_vacuity, min_support)
                    if constraint_str:
                        res_value = {
                            "template": template_str, "activation": couple[0], "target": couple[1],
                            "act_cond": act_cond, "trg_cond": trg_cond, "time_cond": time_cond
                        }
                        self.query_checking_results[constraint_str] = res_value
                        if return_first:
                            return self.query_checking_results

            else:   # unary template
                constraint['condition'] = (act_cond, time_cond)
                for activity in activations_to_check:
                    constraint['attributes'] = activity

                    constraint_str = query_constraint(self.log, constraint, consider_vacuity, min_support)
                    if constraint_str:
                        res_value = {
                            "template": template_str, "activation": activity,
                            "act_cond": act_cond, "time_cond": time_cond
                        }
                        self.query_checking_results[constraint_str] = res_value
                        if return_first:
                            return self.query_checking_results

        return self.query_checking_results

    def filter_query_checking(self, queries) -> list[list[str]]:
        """
        The function outputs, for each constraint of the query checking result, only the elements of the constraint
        specified in the 'queries' list.

        Parameters
        ----------
        queries : list[str]
            elements of the constraint that the user want to retain from query checking result. Choose one (or more)
            elements among: 'template', 'activation', 'target'.

        Returns
        -------
        assignments
            list containing an entry for each constraint of query checking result. Each entry of the list is a list
            itself, containing the queried constraint elements.
        """
        if self.query_checking_results is None:
            raise RuntimeError("You must run a query checking task before.")
        if len(queries) == 0 or len(queries) > 3:
            raise RuntimeError("The list of queries has to contain at least one query and three queries as maximum")
        assignments = []
        for constraint in self.query_checking_results.keys():
            tmp_answer = []
            for query in queries:
                try:
                    tmp_answer.append(self.query_checking_results[constraint][query])
                except KeyError:
                    print(f"{query} is not a valid query. Valid queries are template, activation, target.")
                    sys.exit(1)
            assignments.append(tmp_answer)
        return assignments

    # FUNCTIONS FOR PRINTING RESULTS ##############
    def print_conformance_results(self):
        if self.conformance_checking_results is None:
            raise RuntimeError("You must run conformance checking before!")

        for key, value in self.conformance_checking_results.items():
            print('Trace ID: ' + str(key[0]) + ' - "' + key[1] + '"')
            for item in value.items():
                print('\t' + item[1].state + '\ton ' + item[0])
            print()
