from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask

"""
Initializes class QueryChecking, inheriting from class PMTask

Parameters
-------
    PMTask
        inheriting from PMTask
        
Attributes
-------
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
"""

class QueryChecking(PMTask):

    def __init__(self):
        self.consider_vacuity: bool
        self.template_str: str = None
        self.max_declare_cardinality: int = 1
        self.activation: str = None
        self.target: str = None
        self.act_cond: str = None
        self.trg_cond: str = None
        self.time_cond: str = None
        self.min_support: float = 1.0
        PMTask.__init__(self)

    @abstractmethod
    def run(self):
        pass
