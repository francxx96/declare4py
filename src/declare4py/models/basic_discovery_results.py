from _future_ import annotations

from src.declare4py.checker_result import CheckerResult
from src.declare4py.log_utils.log_analyzer import LogAnalyzer

"""
Initializes class BasicDiscoveryResults

Attributes
-------
    dict_results : dict
        dictionary of conformance checking results
"""


class BasicDiscoveryResults:

    def __init__(self, dict_results: dict):
        self.basic_discovery_results: dict = dict_results
        self.log: LogAnalyzer = None

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
        if self.basic_discovery_results is None:
            raise RuntimeError("You must run a Discovery task before.")
        if not 0 <= min_support <= 1:
            raise RuntimeError("Min. support must be in range [0, 1].")

        result = {}

        for key, val in self.basic_discovery_results.items():
            support = len(val) / len(self.log)
            if support >= min_support:
                result[key] = support

        if output_path is not None:
            with open(output_path, 'w') as f:
                f.write("activity " + "\nactivity ".join(self.get_log_alphabet_activities()) + "\n")
                f.write('\n'.join(result.keys()))

        return result
