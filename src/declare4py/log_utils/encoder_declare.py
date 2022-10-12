import pandas as pd
from mlxtend.preprocessing import TransactionEncoder


class EncoderDeclare:
    """
            Wrapper that collects the computed binary encoding for the input log.

            Attributes
            ----------
            binary_encoded_log : DataFrame
                the binary encoded version of the input log
        """
    def __init__(self):
        self.binary_encoded_log = None

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