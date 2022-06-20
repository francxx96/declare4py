from src.api.declare4py import Declare4Py
import pdb
log_path = "Sepsis Cases.xes.gz"
model_path = "declare_models/data_model.decl"


checker = Declare4Py()


checker.parse_xes_log(log_path)
act = checker.get_log_activities()
res = checker.get_log_payload()
checker.parse_decl_model(model_path)
ww = checker.get_trace_keys()
first_constraint = checker.get_model_constraints()[0]
dd=checker.activities_log_projection()
pdb.set_trace()
model_check_res = checker.conformance_checking(consider_vacuity=True)

model_check_res[(1049, 'LNA')]

checker.print_conformance_results()

# print(checker.get_supported_templates())
