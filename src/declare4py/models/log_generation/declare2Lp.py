"""
TODO: LP doesn't support float, thus we hav to Scale floating attribute bounds to the lowest integers
"""
import typing
from typing import Dict

from src.declare4py.models.log_generation.declare_constraint_resolver import DeclareConstraintConditionResolver
from src.declare4py.models.log_generation.declare_model import DeclareEventAttributeType, DeclareEventValueType, \
    ConstraintTemplates, DeclareModel


class LpBuilder:
    lines: [str] = []
    attributes_values: [str] = []
    templates_s: [str] = []

    def define_predicate(self, name: str, predicate_name: str):
        self.lines.append(f'{predicate_name}({name.lower()}).')

    def define_predicate_attr(self, name: str, attr: str):
        self.lines.append(f'has_attribute({name.lower()}, {attr}).')

    def set_attr_value(self, attr: str, value: DeclareEventAttributeType):
        val_lp = ""
        if value.is_range_typ:
            v = value.value.replace("integer", "").replace("float", "").replace("between", "") \
                .replace("and", "") \
                .replace("  ", " ") \
                .strip()
            v = v.split(" ")
            if value.typ == DeclareEventValueType.FLOAT:
                v[0] = round(v[0])
                v[1] = round(v[1])
            val_lp = f'value({attr}, {v[0]}..{v[1]}).'
        elif value.typ == DeclareEventValueType.ENUMERATION:
            lst = value.value.split(",")
            value_in_lp = []
            for s in lst:
                s = s.strip()
                val_lp_1 = f'value({attr}, {s}).'
                if val_lp_1 not in self.attributes_values:
                    value_in_lp.append(val_lp_1)
                val_lp = "\n".join(value_in_lp)
        else:
            val_lp = f'value({attr}, {value.value}).'

        if val_lp not in self.attributes_values:
            self.attributes_values.append(val_lp)

    def add_template(self, name, ct: ConstraintTemplates, idx: int,
                     props: Dict[str, typing.List[DeclareEventAttributeType]]):
        self.templates_s.append(f"template({idx},\"{name}\").")
        dc = DeclareConstraintConditionResolver()
        ls = dc.resolve_to_asp(ct, props, idx)
        if ls and len(ls) > 0:
            self.templates_s = self.templates_s + ls

    def __str__(self) -> str:
        line = "\n".join(self.lines)
        line = line + "\n\n" + "\n".join(self.attributes_values)
        line = line + "\n\n" + "\n".join(self.templates_s)
        return line


class Declare2lp:
    lp: LpBuilder

    def __init__(self) -> None:
        self.lp = LpBuilder()

    def from_decl(self, model: DeclareModel) -> LpBuilder:
        keys = model.events.keys()
        for k in keys:
            obj = model.events[k]
            obj_typ = obj["object_type"]
            self.lp.define_predicate(k, obj_typ)
            props = obj["props"]
            for attr in props:
                self.lp.define_predicate_attr(k, attr)
                dopt: DeclareEventAttributeType = props[attr]
                self.lp.set_attr_value(attr, dopt)
        templates_idx = 0
        # for tmp_name in model.templates_dict.keys():
        for ct in model.templates:
            self.lp.add_template(ct.template_name, ct, templates_idx, model.attributes)
            # template_line.append(f"template({templates_idx},\"{tmp_name}\")")
            templates_idx = templates_idx + 1
        return self.lp
