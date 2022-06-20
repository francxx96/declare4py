from src.api.declare4py import Declare4Py
import pdb
log_path = "test/Sepsis Cases.xes.gz"
model_path = "test/declare_models/data_model.decl"


checker = Declare4Py()


checker.parse_xes_log(log_path)
'''act = checker.get_log_activities()
res = checker.get_log_payload()
checker.parse_decl_model(model_path)
ww = checker.get_trace_keys()
first_constraint = checker.get_model_constraints()[0]
dd=checker.activities_log_projection()
pdb.set_trace()
model_check_res = checker.conformance_checking(consider_vacuity=True)

model_check_res[(1049, 'LNA')]

checker.print_conformance_results()'''

checker.compute_frequent_itemsets(min_support=0.99)
ee=checker.discovery(consider_vacuity=True, max_declare_cardinality=2, output_path="output.decl")

ww=checker.filter_discovery(min_support=1, output_path="filtered.decl")

