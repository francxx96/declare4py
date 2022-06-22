from src.api.declare4py import Declare4Py
import time

log_path = "test/Sepsis Cases.xes.gz"
model_path = "test/test_models/model4.decl"
d4py = Declare4Py()
d4py.parse_xes_log(log_path)
test = "discovery"

start = time.time()
if test == "checking":
    d4py.parse_decl_model(model_path)
    d4py.conformance_checking(consider_vacuity=True)
elif test == "discovery":
    d4py.compute_frequent_itemsets(min_support=0.8, len_itemset=2)
    d4py.discovery(consider_vacuity=True, max_declare_cardinality=2)
    d4py.filter_discovery(min_support=0.5, output_path='eh.decl')
else:
    pass
end = time.time()
print(f"{end - start}")
