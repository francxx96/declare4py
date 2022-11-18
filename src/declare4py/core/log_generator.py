from abc import abstractmethod

from src.declare4py.core.pm_task import PMTask
from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.log_utils.ltl_model import LTLModel

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

    def __init__(self, num_traces: int, min_event: int, max_event: int, log: LogAnalyzer, ltl_model: LTLModel):
        super().__init__(log, ltl_model)
        self.log_length: int = num_traces
        self.max_events: int = min_event
        self.min_events: int = max_event

    @abstractmethod
    def run(self):
        pass

