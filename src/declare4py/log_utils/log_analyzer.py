import pandas as pd
import pm4py
from mlxtend.frequent_patterns import fpgrowth, apriori


class LogAnalyzer:
    """
        Wrapper that collects the input log, the computed binary encoding and frequent item sets
        for the input log.

        Attributes
        ----------
        log : EventLog
            the input event log parsed from a XES file
        log_length : int
            the trace number of the input log
        frequent_item_sets : DataFrame
        list of the most frequent item sets found along the log traces, together with their support and length
    """

    def __init__(self):
        self.log = None
        self.log_length = None
        self.frequent_item_sets = None

    # LOG MANAGEMENT UTILITIES
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