import sys

from _future_ import annotations

"""
Initializes class QueryCheckingResults

Attributes
--------
    dict_results : dict
        dictionary of conformance checking results

"""


class BasicQueryCheckingResults:

    def __init__(self, dict_results: dict):
        self.basic_query_checking_results: dict = dict_results

    def full_results(self) -> dict:
        for k, v in self.basic_query_checking_results.items():
            dict[k] = v
        return dict

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
        if self.basic_query_checking_results is None:
            raise RuntimeError("You must run a query checking task before.")
        if len(queries) == 0 or len(queries) > 3:
            raise RuntimeError("The list of queries has to contain at least one query and three queries as maximum")
        assignments = []
        for constraint in self.basic_query_checking_results.keys():
            tmp_answer = []
            for query in queries:
                try:
                    tmp_answer.append(self.basic_query_checking_results[constraint][query])
                except KeyError:
                    print(f"{query} is not a valid query. Valid queries are template, activation, target.")
                    sys.exit(1)
            assignments.append(tmp_answer)
        return assignments
