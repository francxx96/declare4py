from __future__ import annotations

import warnings
from enum import Enum
import typing
import re

from src.declare4py.models.log_generation.declare_constraint_resolver import DeclareConstraintResolver
from src.declare4py.models.log_generation.declare_model import DeclareModel, DeclareEventAttributeType, \
    DeclareEventValueType

"""
Declare Model Syntax


[exmample.decl]

activity A                                  # defining an Object/Event.
bind A: grade                               # defining an attribute or property. Line starting with "bind" word
bind A: mark, name                          # defining multiple attributes or properties together
activity B
bind B: grade, mark, name
grade, mark: integer between 1 and 5        # multiple props/attrs declaration as far as they share the same declaration
                                            # type. the types can be: integer, float, enumeration
# mark: float between 2 and 9.5             # start '#' char we can consider line as comment
name: x, y, z, v                            # data declaration as enumeration 

# constraints template are pre-defined and after template name defined, it can have also 3 or
# 2 pipes( | | | ) which defines constraints
Response[A, B] |A.grade = 3 |B.grade > 5 |1,5,s
Response[A, B] |A.grade <= 4 | A.name is y | 0,s

---
        
An object or Event can be defined in the declare(.decl) using a standalone line 
and specifying
 `[typeOfObjectOrEvent] [nameInUppercase]`
for example as we can see above in the example
 `activity A`

An Object/Event can has/have also properties:
 `bind [nameOfObject]: [newPropertyName]`
 I.e in above example
 `bind A: grade`
line starting from "bind" used to create new attributes or properties.(A.mark) 


Declare has some predefined Constraint Templates and some of them are described here in this document on page 7:
@article{maggidata,
  title={Data-aware Synthetic Log Generation for De-clarative Process Models},
  author={Maggi, Fabrizio Maria and Di Francescomarino, Chiara and Ghidini, Chiara}
}

Declaration can have types such as: integer, float, enumeration for now.
Moreover, integer and float can have ranges defined as  `integer between 5 and 9` or `float between 2.9 and 6`.
A label can be check in constraint using `is` keyword and can
be negate `is not`. ie. `template[a,b] |a is x| b is not x |1,2,s`


------

correction

conditions can have only A. T. A= activation key, T= target

time condtion...  1,5s  from 1 to 5second.... After applied activation condition and T=target
 condition should be in range in given timestramp (1s to 5s)

SUGGESTIONS OR DOUBTS
 - comment lines starting from `#`
 - have some reserve words such as integer, float, between, and
 
"""


class DeclareReserved:
    words = ["is", "not", "in", "between", "integer", "float", "enumeration", "and"]
    condition_symbols = [">", "<", "=", "is", ">=", "<=", "is not", "in", "not"]


class DeclareLineDefinition(Enum):
    DEFINE_EVENT_LINE = 1
    DEFINE_PROP_LINE = 2  # TODO: fix name
    DEFINE_PROP_VALUE_LINE = 3  # Constraints
    DEFINE_CONSTRAINT_TEMPLATE = 4


class DeclareParser:
    CONSTRAINTS_TEMPLATES_PATTERN = "^(.*)\[(.*)\]\s*(.*)$"
    declare_content: [str]
    model: DeclareModel
    acts = {}  # { act_name: [] }

    def __init__(self, content: typing.Union[str, typing.List[str]]):
        self.load_declare_content(content)
        self.model = DeclareModel()

    def load_declare_content(self, content: typing.Union[str, typing.List[str]]):
        if isinstance(content, str):
            self.declare_content = content.split('\n')
        else:
            self.declare_content = content
        self.model = DeclareModel()

    def parse(self) -> DeclareModel:
        line_index = 0
        for line in self.declare_content:
            line = line.strip('\n').strip()  # clear the string, removing whitespace
            line_index = line_index + 1
            if len(line) > 0 and not line.startswith("#"):
                self.parse_line(line, line_index)
        return self.model

    def parse_line(self, line: str, line_idx: int):
        line = line.strip()
        if self.is_event_name_definition(line):
            self.__parse_event_definition(line, line_idx)
        elif self.is_event_attributes_definition(line):
            self.__parse_attributes_definition(line, line_idx)
        elif self.is_events_attrs_value_definition(line):
            self.__parse_attrs_values_definition(line, line_idx)
        elif self.is_constraint_template_definition(line):
            self.__parse_constraint_template(line)
        else:
            raise ValueError(f"Unable to parse the line[{line_idx}]")

    def is_event_name_definition(self, line: str) -> bool:
        x = re.search("^[\w]+ [\w ]+$", line, re.MULTILINE)
        return x is not None

    def is_event_attributes_definition(self, line: str) -> bool:
        # x = re.search("^bind [a-zA-Z_]+[0-9]* *: *[\w, ]+$", line, re.MULTILINE)  # not good for "bind: org:resource"
        x = re.search("^bind (.*?)+$", line, re.MULTILINE)
        return x is not None

    def is_events_attrs_value_definition(self, line: str) -> bool:
        # x = re.search("^(?!bind)[a-zA-Z_, ]+[0-9]* *: *[\w, ]+", line, re.MULTILINE)
        """
        categorical: c1, c2, c3
        categorical: group1:v1, group1:v2, group3:v1       <-------- Fails to parse this line
        integer: integer between 0 and 100
        org:resource: 10
        org:resource, org:vote: 10
        org:vote, grade: 9
        org:categorical: integer between 0 and 100
        categorical: integer between 0 and 100
        base, mark: integer between 0 and 100
        org:res, grade, concept:name: integer between 0 and 100
        :param line: declare line
        :return:
        """
        x = re.search("^(?!bind)([a-zA-Z_,0-9: ]+) *(: *[\w, ]+)$", line, re.MULTILINE)
        if x is None:
            return False
        groups_len = len(x.groups())
        return groups_len >= 2

    def is_constraint_template_definition(self, line: str) -> bool:
        x = re.search(self.CONSTRAINTS_TEMPLATES_PATTERN, line, re.MULTILINE)
        return x is not None

    def __parse_event_definition(self, line: str, line_idx: int, strict=True):
        var_declaration: [str] = line.split(' ')  # TODO ...
        if len(var_declaration) != 2:
            raise ValueError(f"Error in line {line_idx}: {line}.\n\tCan have only two words for defining an event: "
                             f"`EventType EventName`")
        event_name = var_declaration[1].strip()
        event_type = var_declaration[0].strip()
        if event_name in self.model.events:
            raise KeyError(f"Error in line {line_idx}: {line}.\n\tMultiple times declaring [{event_name}] event name")
        if strict and self.__is_reserved_keyboard(event_name):
            raise NameError(f"""`{event_name}` is reserved. Cannot be used.""")
        if strict and self.__is_reserved_keyboard(event_type):
            raise NameError(f"""Type of object defined(`{event_type}`) is already reserved.""")
        self.model.events[event_name] = {"object_type": event_type}

    def __parse_attributes_definition(self, line: str, line_idx: int, strict=False):
        arr = line.replace('bind', '').strip().split(':', maxsplit=1)  # LINE: bind B: grade, mark, name
        event_name = arr[0].strip()  # B
        propsOrAttrs = arr[1].strip().split(',')  # grade, mark, name
        if event_name not in self.model.events:
            raise NameError(f"""Error in line: {line_idx}""")
        obj = self.model.events[event_name]
        if "props" not in obj:
            obj["props"]: typing.Dict[str, DeclareEventAttributeType] = {}
        props = obj["props"]
        for p in propsOrAttrs:
            p = p.strip()
            if strict and self.__is_reserved_keyboard(p):
                raise NameError(f"""Type of object property defined(`{p}`) is already reserved.""")
            props[p] = DeclareEventAttributeType()
            if p in self.model.attributes:
                sp = self.model.attributes[p]
                sp.append(props[p])
            else:
                self.model.attributes[p] = [props[p]]

    def __parse_attrs_values_definition(self, line: str, line_idx: int):
        """
        Parse declare lines of assigning values to attributes

        possible lines for assigning values to attributes
            categorical: c1, c2, c3
            categorical: group1:v1, group1:v2, group3:v1       <-------- Fails to parse this line
            integer: integer between 0 and 100
            org:resource: 10
            org:resource, org:vote: 10
            org:vote, grade: 9
            org:categorical: integer between 0 and 100
            categorical: integer between 0 and 100
            base, mark: integer between 0 and 100
            org:res, grade, concept:name: integer between 0 and 100

        We use ": " (column with space after) to split the line in order have two parts.
        Assume that on the left part are defined the attributes and on the right side the values
        :param line: declare line
        :return: void
        """

        arr = line.strip().split(': ')  # grade, mark: integer between 1 and 5
        if len(arr) != 2:
            raise ValueError(f"Failed to parse in line {line_idx}: {line}")
        props = arr[0].strip().split(", ")  # TODO: still to improve  maybe using encoding to avoid if attribute name contains "," char.
        value = arr[1].strip()  # TODO: don't know yet how can be improved if there is an complex enum value "gro,up:v2"
        dopt = self.__parse_attr_value(value, line_idx)
        for p in props:
            p = p.strip()
            if p not in self.model.attributes:
                warnings.warn(f""" "{p}" attribute not defined. Found in line[{line_idx}] "{line}" """)
                continue
            props_of_obj = self.model.attributes[p]
            if props_of_obj:
                for pr in props_of_obj:
                    pr.typ = dopt.typ
                    pr.is_range_typ = dopt.is_range_typ
                    pr.value = dopt.value

    def __parse_attr_value(self, value: str, idx: int) -> DeclareEventAttributeType:
        # value: integer between 1 and 5     #  <--- integer
        # value: float between 1 and 5       #  <--- float
        # value: x, y, z, v                  #  <--- enumeration
        integer_range_rx = "^integer[ ]+between[ ]+[+-]?\d+[ ]+and[ ]+[+-]?\d+$"
        float_range_rx = "^float[ ]+between[ ]+[+-]?\d+(\.\d+)?[ ]+and[ ]+[+-]?\d+(\.\d+)?$"
        # enume_rx = "^[\w]+(,[ ]*[\w.]+)*$"  # matches -> [xyz, xyz, dfs], [12,45,78.54,454]
        enume_rx = "^[\w,:]+ *(, *[\w:]+)*$"  # matches -> [xyz, xyz, dfs], [12,45,78.54,454]
        value = value.strip()
        dopt = DeclareEventAttributeType()
        dopt.value = value
        if re.search(integer_range_rx, value, re.MULTILINE):
            dopt.typ = DeclareEventValueType.INTEGER
            dopt.is_range_typ = True
        elif re.search(float_range_rx, value, re.MULTILINE):  # float
            dopt.typ = DeclareEventValueType.FLOAT
            dopt.is_range_typ = True
        elif re.search(enume_rx, value, re.MULTILINE):  # enumeration
            dopt.typ = DeclareEventValueType.ENUMERATION
            dopt.is_range_typ = False
        else:
            x = re.search("^[+-]?\d+$", value, re.MULTILINE)
            if x:
                dopt.typ = DeclareEventValueType.INTEGER
                dopt.is_range_typ = False
            elif re.search("^[+-]?\d+(\.\d+)?$", value, re.MULTILINE):
                dopt.typ = DeclareEventValueType.FLOAT
                dopt.is_range_typ = False
            else:
                raise ValueError(f"""Unable to parse {value} in line {idx}""")
        return dopt

    def __parse_constraint_template(self, line: str):
        # Response[A, B] |A.grade = 3 |B.grade > 5 |1,5,s
        d = DeclareConstraintResolver()
        ct = d.parse_template(line)
        if ct:
            self.model.templates.append(ct)
            lis = []
            if ct.template_name in self.model.templates_dict:
                lis = self.model.templates_dict[ct.template_name]
            else:
                self.model.templates_dict[ct.template_name] = lis
            lis.append(ct)

    def __is_reserved_keyboard(self, word: str) -> bool:
        ws = DeclareReserved.words
        return word in ws

