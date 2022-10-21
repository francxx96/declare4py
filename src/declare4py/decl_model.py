class DeclModel(object):
    def __init__(self):
        self.activities = []
        self.constraints = []
        self.checkers = []
    
    def set_constraints(self):
        constraint_str = ''
        if len(self.checkers) > 0:
            for checker in self.checkers:
                constraint_str = checker["template"].templ_str + '[' + checker["attributes"] + '] |' \
                                 + ' |'.join(checker["condition"])
                self.constraints.append(constraint_str)
                
    def get_decl_model_constraints(self):
        return self.constraints

    def get_model_activities(self) -> list[str]:
        """
        Return the activities contained in the DECLARE model.

        Returns
        -------
        activities
            list of activity names contained in the DECLARE model.
        """
        if self.model is None:
            raise RuntimeError("You must load a DECLARE model before.")

        return self.model.activities

    def get_model_constraints(self) -> list[str]:
        """
        Return the constraints contained in the DECLARE model.

        Returns
        -------
        activities
            list of constraints contained in the DECLARE model.
        """
        if self.model is None:
            raise RuntimeError("You must load a DECLARE model before.")

        return self.model.get_decl_model_constraints()