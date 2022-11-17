from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask

"""
Initializes class LogGenerator, inheriting from class PMTask

Parameters
-------
log_length
    object of type int
PMTask
    inheriting from PMTask
"""


class LogGenerator(PMTask):

    def __init__(self):
        self.log_length: int = None
        self.max_events: int = None
        self.min_events: int = None

    @abstractmethod
    def run(self):
        pass

