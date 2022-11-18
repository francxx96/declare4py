try:
    from _future_ import annotations
except:
    pass

import pandas as pd
import pm4py
from mlxtend.frequent_patterns import fpgrowth, apriori
from mlxtend.preprocessing import TransactionEncoder
from pm4py.objects.log import obj as lg


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
        binary_encoded_log : DataFrame
                the binary encoded version of the input log
    """

    def __init__(self):
        self.log: lg.EventLog = None
        self.log_length = None
        self.frequent_item_sets = None
        self.binary_encoded_log = None

    # LOG MANAGEMENT UTILITIES
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
        if len_itemset < 1:
            raise RuntimeError(f"The parameter len_itemset must be greater than 0.")
        else:
            self.frequent_item_sets = frequent_itemsets[(frequent_itemsets['length'] <= len_itemset)]

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
