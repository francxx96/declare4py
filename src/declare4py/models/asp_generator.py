import pandas as pd

from src.declare4py.core.log_generator import LogGenerator


class AspGenerator:

    def __init__(self):
        LogGenerator.__init__(self)

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
