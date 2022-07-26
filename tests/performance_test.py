import os
from declare4py.declare4py import Declare4Py
import time

import sys
sys.path.append("..")

log_path = os.path.join("..", "tests", "Sepsis Cases.xes.gz")
log_path = os.path.join("..", "tests", "reimb.xes.gz")
model_path = os.path.join("..", "tests", "test_models_reimb", "model1.decl")
d4py = Declare4Py()
d4py.parse_xes_log(log_path)
test = "checking"

start = time.time()
if test == "checking":
    d4py.parse_decl_model(model_path)
    d4py.conformance_checking(consider_vacuity=True)
elif test == "discovery":
    d4py.compute_frequent_itemsets(min_support=0.8, len_itemset=2)
    d4py.discovery(consider_vacuity=True, max_declare_cardinality=2)
elif test == "query":
    #d4py.query_checking(consider_vacuity=False, template_str='Chain Response', activation='IV Antibiotics',
    #                    act_cond='A.org:group is A', min_support=0.042, return_first=False)
    d4py.query_checking(consider_vacuity=False, template_str='Chain Response', activation='IV Antibiotics',
                        act_cond='A.org:group is A', min_support=0.042, return_first=False)
else:
    pass
end = time.time()
print(f"{end - start}")
