from _future_ import annotations

"""
Provides basic discovery functionalities

Parameters
--------
    Discovery
        inherit class init

Attributes
--------


"""
from src.declare4py.api_functions import check_trace_conformance
from src.declare4py.checker_result import CheckerResult
from src.declare4py.core.discovery import Discovery
from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.models.discovery_results import BasicDiscoveryResults
from src.declare4py.log_utils.parsers.declare.decl_model import DeclModel
from src.declare4py.mp_constants import Template, TraceState


class BasicMPDeclareDiscovery(Discovery):

    def __init__(self, consider_vacuity, support, max_declare_cardinality):
        super().__init__(consider_vacuity, support, max_declare_cardinality)
        output_path: str = None

    def run(self, consider_vacuity: bool, max_declare_cardinality: int = 3, output_path: str = None) \
            -> BasicDiscoveryResults:
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

        Discovery.discovery_results = {}

        for item_set in self.frequent_item_sets['itemsets']:
            length = len(item_set)

            if length == 1:
                for templ in Template.get_unary_templates():
                    constraint = {"template": templ, "activities": ', '.join(item_set), "condition": ("", "")}
                    if not templ.supports_cardinality:
                        self.discovery_results |= self.discover_constraint(self.log, constraint, consider_vacuity)
                    else:
                        for i in range(max_declare_cardinality):
                            constraint['n'] = i + 1
                            self.discovery_results |= self.discover_constraint(self.log, constraint, consider_vacuity)

            elif length == 2:
                for templ in Template.get_binary_templates():
                    constraint = {"template": templ, "activities": ', '.join(item_set), "condition": ("", "", "")}
                    self.discovery_results |= self.discover_constraint(self.log, constraint, consider_vacuity)

                    constraint['activities'] = ', '.join(reversed(list(item_set)))
                    self.discovery_results |= self.discover_constraint(self.log, constraint, consider_vacuity)

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

    def discover_constraint(log: LogAnalyzer, constraint: str, consider_vacuity: bool):
        # Fake model composed by a single constraint
        model = DeclModel()
        model.constraints.append(constraint)

        discovery_res = {}

        for i, trace in enumerate(log):
            trc_res = check_trace_conformance(trace, model, consider_vacuity)
            if not trc_res:     # Occurring when constraint data conditions are formatted bad
                break

            constraint_str, checker_res = next(iter(trc_res.items()))  # trc_res will always have only one element inside
            if checker_res.state == TraceState.SATISFIED:
                new_val = {(i, trace.attributes['concept:name']): checker_res}
                if constraint_str in discovery_res:
                    discovery_res[constraint_str] |= new_val
                else:
                    discovery_res[constraint_str] = new_val

        return discovery_res
