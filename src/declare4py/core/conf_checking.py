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

    def __init__(self):
        self.consider_vacuity: bool
        PMTask.__init__(self)

    @abstractmethod
    def run(self):
        pass
