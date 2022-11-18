
"""
Initializes super class PMTask

Attributes
-------
    log_analyzer : LogAnalyzer

    decl_model : DeclareModel
    
"""

from src.declare4py.log_utils.parsers.declare.decl_model import DeclModel
from src.declare4py.log_utils.log_analyzer import LogAnalyzer
from src.declare4py.log_utils.ltl_model import LTLModel


class PMTask:

    def __init__(self, log: LogAnalyzer, ltl_model: LTLModel):
        self.log_analyzer: LogAnalyzer = log
        self.decl_model: DeclModel = ltl_model

