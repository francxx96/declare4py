class DeclModel(object):
    def __init__(self):
        self.activities = []
        self.serialized_constraints = []
        self.constraints = []
        
    
    def set_constraints(self):
        constraint_str = ''
        if len(self.constraints) > 0:
            for constraint in self.constraints:

                constraint_str = constraint['template'].templ_str
                if constraint['template'].supports_cardinality:
                    constraint_str += str(constraint['n'])
                constraint_str += '[' + ", ".join(constraint["activities"]) + '] |' + ' |'.join(constraint["condition"])
                self.serialized_constraints.append(constraint_str)
                
    def get_decl_model_constraints(self):
        return self.serialized_constraints
