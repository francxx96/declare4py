
"""
Initializes super class PMTask

Attributes
-------
    log_analyzer : LogAnalyzer

    decl_model : DeclareModel
    
"""
from src.declare4py.log_utils.decl_model import DeclModel
from src.declare4py.log_utils.log_analyzer import LogAnalyzer


class PMTask:

    def __init__(self):
        self.log_analyzer: LogAnalyzer = None
        self.decl_model: DeclModel = None

