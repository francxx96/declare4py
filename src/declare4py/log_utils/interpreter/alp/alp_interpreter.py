
"""
Abductive logic programming (ALP) is a high-level knowledge-representation framework that can be used to solve
 problems declaratively based on abductive reasoning.
"""
from src.declare4py.log_utils.interpreter.alp.declare_constraint_resolver import DeclareModalConstraintConditionResolver
from src.declare4py.log_utils.parsers.declare.decl_model import DeclareModelAttributeType, DeclareTemplateModalDict, \
    DeclModel


class ALPModel:
    lines: [str] = []
    values_assignment: [str] = []
    attributes_values: [str] = []
    templates_s: [str] = []

    def __init__(self):
        self.lines = []
        self.values_assignment = []
        self.attributes_values = []
        self.templates_s = []

    def define_predicate(self, name: str, predicate_name: str):
        self.lines.append(f'{predicate_name}({name.lower()}).')

    def define_predicate_attr(self, event_name: str, attr_name: str):
        self.lines.append(f'has_attribute({event_name.lower()}, {attr_name}).')
        self.values_assignment.append(f'has_attribute({event_name.lower()}, {attr_name}).')

    def set_attr_value(self, attr: str, value: dict):
        if value["value_type"] == DeclareModelAttributeType.INTEGER:
            self.add_attribute_value_to_list(f'value({attr}, {value["value"]}).')
        elif value["value_type"] == DeclareModelAttributeType.FLOAT:
            self.add_attribute_value_to_list(f'value({attr}, {value["value"]}).')
        elif value["value_type"] == DeclareModelAttributeType.INTEGER_RANGE:
            frm, til = self.__parse_range_value(value["value"])
            self.add_attribute_value_to_list(f'value({attr}, {frm}..{til}).')
        elif value["value_type"] == DeclareModelAttributeType.FLOAT_RANGE:
            frm, til = self.__parse_range_value(value["value"])
            # TODO: scale float values
            self.add_attribute_value_to_list(f'value({attr}, {frm}..{til}).')
        elif value["value_type"] == DeclareModelAttributeType.ENUMERATION:
            val = value["value"].split(",")
            val = [v.strip().lower() for v in val]
            for s in val:
                self.add_attribute_value_to_list(f'value({attr}, {s}).')

    def add_attribute_value_to_list(self, value: str):
        if value not in self.attributes_values:
            self.attributes_values.append(value)

    def __parse_range_value(self, value: str):
        v = value.lower().replace("integer", "")\
            .replace("float", "")\
            .replace("between", "") \
            .replace("and", "") \
            .replace("  ", " ") \
            .strip()
        (frm, til) = v.split(" ")
        return frm, til

    def add_template(self, name, ct: DeclareTemplateModalDict, idx: int, props: dict[str, dict]):
        self.templates_s.append(f"template({idx},\"{name}\").")
        dc = DeclareModalConstraintConditionResolver()
        ls = dc.resolve_to_asp(ct, props, idx)
        if ls and len(ls) > 0:
            self.templates_s = self.templates_s + ls + ["\n"]

    def to_str(self):
        return self.__str__()

    def __str__(self) -> str:
        line = "\n".join(self.lines)
        line = line + "\n\n" + "\n".join(self.attributes_values)
        line = line + "\n\n" + "\n".join(self.templates_s)
        return line

    def __repr__(self):
        return f"{{ \"total_facts\": \"{len(self.lines) - len(self.values_assignment)}\", \"values_assignment\": \"{len(self.values_assignment)}\" }}"


class ALPInterpreter:
    alp_model: ALPModel

    def __init__(self) -> None:
        self.alp_model = ALPModel()

    def from_decl_model(self, model: DeclModel) -> ALPModel:
        keys = model.parsed_model
        for k in keys.events:
            event = keys.events[k]
            self.alp_model.define_predicate(event.name, event.event_type)
            attrs = event.attributes
            for attr in attrs:
                self.alp_model.define_predicate_attr(event.name, attr)
                dopt = attrs[attr]
                self.alp_model.set_attr_value(attr, dopt)
        templates_idx = 0
        for ct in model.parsed_model.templates:
            self.alp_model.add_template(ct.template_name, ct, templates_idx, model.parsed_model.attributes_list)
            # template_line.append(f"template({templates_idx},\"{tmp_name}\")")
            templates_idx = templates_idx + 1
        return self.alp_model

