from _future_ import annotations
import re
import sys
from abc import ABC

from numpy import product, ceil

from src.declare4py.api_functions import check_trace_conformance
from src.declare4py.core.query_checking import QueryChecking
from src.declare4py.log_utils.decl_model import DeclModel
from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.models.basic_query_checking_results import BasicQueryCheckingResults
from src.declare4py.mp_constants import Template, TraceState

"""
Class used to provide basic query checking functionalities

Parameters
--------
    QueryChecking
        inherits attributes from the QueryChecking class

Attributes
--------
    QueryChecking init
        inherits init attributes form the QueryChecking class
        
    query_checking_results : dict
        output type for this class
        
        
"""


class BasicMPDeclareQueryChecking(QueryChecking, ABC):

    def __init__(self, consider_vacuity, template_str, max_declare_cardinality, activation, target, act_cond, trg_cond, time_cond, min_support):
        super().__init__(consider_vacuity, template_str, max_declare_cardinality, activation, target, act_cond, trg_cond, time_cond, min_support)
        self.query_checking_results: dict = None

    def run(self, consider_vacuity: bool,
                       template_str: str = None, max_declare_cardinality: int = 1,
                       activation: str = None, target: str = None,
                       act_cond: str = None, trg_cond: str = None, time_cond: str = None,
                       min_support: float = 1.0) -> BasicQueryCheckingResults:
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
            activation condition to evaluate. It has to be written by following the DECLARE standard format.

        trg_cond : str, optional
            target condition to evaluate. It has to be written by following the DECLARE standard format.

        time_cond : str, optional
            time condition to evaluate. It has to be written by following the DECLARE standard format.

        min_support : float, optional
            the minimum support that a constraint needs to have to be included in the result (default 1).

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
                            templates_to_check.append(template.templ_str + str(card + 1))
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
                    constraint['activities'] = ', '.join(couple)

                    constraint_str = self.query_constraint(self.log, constraint, consider_vacuity, min_support)
                    if constraint_str:
                        res_value = {
                            "template": template_str, "activation": couple[0], "target": couple[1],
                            "act_cond": act_cond, "trg_cond": trg_cond, "time_cond": time_cond
                        }
                        self.query_checking_results[constraint_str] = res_value

            else:  # unary template
                constraint['condition'] = (act_cond, time_cond)
                for activity in activations_to_check:
                    constraint['activities'] = activity

                    constraint_str = self.query_constraint(self.log, constraint, consider_vacuity, min_support)
                    if constraint_str:
                        res_value = {
                            "template": template_str, "activation": activity,
                            "act_cond": act_cond, "time_cond": time_cond
                        }
                        self.query_checking_results[constraint_str] = res_value

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

    def query_constraint(log: LogAnalyzer, constraint: str, consider_vacuity: bool, min_support: int):
        # Fake model composed by a single constraint
        model = DeclModel()
        model.constraints.append(constraint)

        sat_ctr = 0
        for i, trace in enumerate(log):
            trc_res = check_trace_conformance(trace, model, consider_vacuity)
            if not trc_res:  # Occurring when constraint data conditions are formatted bad
                break

            constraint_str, checker_res = next(
                iter(trc_res.items()))  # trc_res will always have only one element inside
            if checker_res.state == TraceState.SATISFIED:
                sat_ctr += 1
                # If the constraint is already above the minimum support, return it directly
                if sat_ctr / len(log) >= min_support:
                    return constraint_str
            # If there aren't enough more traces to reach the minimum support, return nothing
            if len(log) - (i + 1) < ceil(len(log) * min_support) - sat_ctr:
                return None

        return None
