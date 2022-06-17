from src.api.declare4py import Declare4Py

log_path = "Sepsis Cases.xes.gz"
model_path = "sepsis model.decl"

checker = Declare4Py()

checker.parse_xes_log(log_path)
checker.parse_decl_model(model_path)
checker.conformance_checking(True)

checker.print_conformance_results()

# print(checker.get_supported_templates())
