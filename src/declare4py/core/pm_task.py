from declare4py.src.declare4py.log_utils.decl_model import DeclModel
from declare4py.src.declare4py.log_utils.log_analyzer import LogAnalyzer

"""
Initializes super class PMTask

Attributes
-------
log_analyzer : LogAnalyzer
    
decl_model : DeclareModel
    
"""
class PMTask:

    def __init__(self):
        self.log_analyzer: LogAnalyzer = None
        self.decl_model: DeclModel = None

