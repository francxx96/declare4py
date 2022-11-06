from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask


class Discovery(PMTask):

    def __init__(self):
        self.consider_vacuity = None
        self.support = None
        self.max_declare_cardinality = None

    @abstractmethod
    def run(self):
        pass

