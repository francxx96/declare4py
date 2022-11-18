from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask

"""
Initializes class ConformanceChecking, inheriting from class PMTask

Parameters
-------
    PMTask
        inheriting from PMTask
Attributes
----------
    consider_vacuity : bool
        True means that vacuously satisfied traces are considered as satisfied, violated otherwise.
        
"""


class ConformanceChecking(PMTask):

    def __init__(self, log, ltl_model):
        self.consider_vacuity: bool
        super().__init__(log, ltl_model)

    @abstractmethod
    def run(self):
        pass
