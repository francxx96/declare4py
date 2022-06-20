from src.api.declare4py import Declare4Py
import time

log_path = "../Sepsis Cases.xes.gz"
model_path = "test_models/model4.decl"

checker = Declare4Py()

start = time.time()

checker.parse_xes_log(log_path)
checker.parse_decl_model(model_path)

model_check_res = checker.conformance_checking(consider_vacuity=True)
#checker.print_conformance_results()

end = time.time()
print(end - start)
