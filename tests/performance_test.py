import os
from declare4py.declare4py import Declare4Py
import time

import sys
sys.path.append("..")

dataset_name = 'BPIC 2020'  # Sepsis, BPIC 2020

if dataset_name == 'Sepsis':
    log_path = os.path.join("..", "tests", "Sepsis Cases.xes.gz")
    model_path = os.path.join("..", "tests", "test_models_sepsis", "model1.decl")
else:
    log_path = os.path.join("..", "tests", "bpic2020.xes.gz")
    model_path = os.path.join("..", "tests", "test_models_bpic2020", "model4.decl")
d4py = Declare4Py()
d4py.parse_xes_log(log_path)
test = "checking"

start = time.time()
if test == "checking":
    d4py.parse_decl_model(model_path)
    d4py.conformance_checking(consider_vacuity=True)
elif test == "discovery":
    d4py.compute_frequent_itemsets(min_support=0.2, len_itemset=2)
    d4py.discovery(consider_vacuity=True, max_declare_cardinality=2)
elif test == "query":
    d4py.query_checking(consider_vacuity=False, template_str='Chain Response', activation='CRP', act_cond=None, min_support=0.8, return_first=False)
    #d4py.query_checking(consider_vacuity=False, template_str='Chain Response', activation='Declaration APPROVED by ADMINISTRATION', act_cond=None, min_support=0.8, return_first=False)
else:
    pass
end = time.time()
print(f"{end - start}")
