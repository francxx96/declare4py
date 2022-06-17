class DeclModel(object):
    def __init__(self):
        self.activities = []
        self.constraints = []
        self.checkers = []
    
    def set_constraints(self):
        constraint_str = ''
        if len(self.checkers) > 0:
            for checker in self.checkers:
                constraint_str = checker["key"] + '[' + checker["attribute"] + '] |' + ' |'.join(checker["condition"])
                self.constraints.append(constraint_str)
                
    def get_decl_model_constraints(self):
        return self.constraints
