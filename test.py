from src.api.declare4py import Declare4Py
import pdb
log_path = "test/Sepsis Cases.xes.gz"
model_path = "test/declare_models/data_model.decl"


d4py = Declare4Py()


d4py.parse_xes_log(log_path)
'''
act = d4py.get_log_activities()
res = d4py.get_log_payload()
d4py.parse_decl_model(model_path)
ww = d4py.get_trace_keys()
first_constraint = d4py.get_model_constraints()[0]
dd=d4py.activities_log_projection()
pdb.set_trace()
model_check_res = d4py.conformance_checking(consider_vacuity=True)

model_check_res[(1049, 'LNA')]

d4py.print_conformance_results()

d4py.compute_frequent_itemsets(min_support=0.9, len_itemset=2)
discovery_results = d4py.discovery(consider_vacuity=True, max_declare_cardinality=2)
print(discovery_results.keys())
decl_constr = 'Responded Existence[ER Sepsis Triage, ER Triage] | | |'
trace_id = (488, 'VR')
print(f"Number of pendings: {discovery_results[decl_constr][trace_id].num_pendings}")
print(f"Number of activations: {discovery_results[decl_constr][trace_id].num_activations}")
print(f"Number of fulfilments: {discovery_results[decl_constr][trace_id].num_fulfillments}")
print(f"Number of violation: {discovery_results[decl_constr][trace_id].num_violations}")
print(f"Truth value of: {discovery_results[decl_constr][trace_id].state}")
'''

model_path = "test/declare_models/data_model.decl"
d4py.parse_decl_model(model_path)
print(d4py.model.__dict__)
