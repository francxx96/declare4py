from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask


class ConformanceChecking(PMTask):

    def __init__(self):
        bool self.consider_vacuity = None
        PMTask.__init__(self)

    @abstractmethod
    def run(self):
        pass
