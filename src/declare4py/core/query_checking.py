from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask


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
