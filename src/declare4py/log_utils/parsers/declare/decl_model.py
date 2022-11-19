from __future__ import annotations

import json
import re
from enum import Enum
import base64
import hashlib
import copy


from abc import ABC, abstractmethod
from src.declare4py.log_utils.ltl_model import LTLModel
# from src.declare4py.log_utils.parsers.declare.declare_parsers_utility import DeclareParserUtility
# from src.declare4py.log_utils.parsers.declare.declare_parsers import DeclareParser
from src.declare4py.mp_constants import Template


class DeclareModelCustomDict(dict, ABC):
    """
    Custom DICT helper class: printable and serializable object
    """
    def __init__(self, *args, **kw):
        super().__init__()
        self.key_value = dict(*args, **kw)

    def __getitem__(self, key):
        self.update_props()
        return self.key_value[key]

    def __setitem__(self, key, value):
        self.key_value[key] = value

    def __iter__(self):
        self.update_props()
        return iter(self.key_value)

    def __len__(self):
        self.update_props()
        return len(self.key_value)

    def __delitem__(self, key):
        self.update_props()
        del self.key_value[key]

    def __str__(self):
        self.update_props()
        # return json.dumps(self, default=lambda o: o.__dict__,)
        # return json.dumps(self.key_value, default=lambda o: self.default_json(o))
        # return json.dumps(self)
        return str(self.key_value)

    def to_json(self, pure=False) -> str:
        if pure:
            return json.dumps(self.key_value)
        st = str(self.key_value).replace("'", '"')
        return str(st)
        # return json.dumps(json.loads(st))
        # return o.__dict__
        # return "33"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def update_props(self):
        pass


class DeclareModelAttributeType(str, Enum):
    INTEGER = "integer"
    FLOAT = "float"
    INTEGER_RANGE = "integer_range"
    FLOAT_RANGE = "float_range"
    ENUMERATION = "enumeration"

    def __str__(self):
        return self.value

    def __repr__(self):
        return "\""+self.__str__()+"\""


class DeclareModelEvent(DeclareModelCustomDict):
    name: str
    event_type: str
    attributes: dict[str, dict]

    def __init__(self):
        super().__init__()
        self.name = ""
        self.event_type = ""
        self.attributes = {}
        self.update_props()

    def update_props(self):
        self.key_value["name"] = self.name
        self.key_value["event_type"] = self.event_type
        self.key_value["attributes"] = self.attributes


class DeclareTemplateModalDict(DeclareModelCustomDict):
    template: Template | None
    template_name: str | None
    activities: str | None
    condition: [str] | None
    template_line: str | None
    condition_line: str | None  # |A.grade < 2  | T.mark > 2|1,5,s

    def __init__(self):
        super().__init__()
        self.template = None
        self.activities = None
        self.condition = None
        self.template_name = None

    def get_conditions(self):
        return self.get_active_condition(), self.get_target_condition(), self.get_time_condition()

    def get_active_condition(self):
        if len(self.condition) > 0:
            return self.condition[0]
        return None

    def get_target_condition(self):
        if len(self.condition) > 1:
            cond_at_1_idx = self.condition[1]
            time_int = r"^[\d.]+,?([\d.]+)?[,]?(s|m|d|h)$"
            is_matched = re.search(time_int, cond_at_1_idx, re.IGNORECASE)
            if is_matched:
                return None
            return self.condition[1]

    def get_time_condition(self):
        if self.contains_interval_condition():
            return self.condition[2]
        return None

    def contains_interval_condition(self) -> bool:
        if self.condition is None:
            return False
        len_ = len(self.condition)
        if len_ != 3:
            return False
        return True
        # if self.condition_line is None:
        #     return False
        # parts = self.condition_line.strip("|").split("|")
        # if len(parts) == 3:
        #     time_int = r"^[\d.]+,?([\d.]+)?[,]?(s|m|d|h)$"
        #     return re.search(time, parts, re.IGNORECASE)
        # return False

    def update_props(self):
        """
        Updates the _dict, so it has updated values when any dict op is occurred
        Returns
        -------

        """
        self.key_value["template"] = self.template
        self.key_value["activities"] = self.activities
        self.key_value["condition"] = self.condition
        self.key_value["template_name"] = self.template_name
        self.key_value["template_line"] = self.template_line
        self.key_value["condition_line"] = self.condition_line


class DeclareParsedModel(DeclareModelCustomDict):
    attributes_list: dict[str, dict] = []
    events: dict[str, DeclareModelEvent] = {}
    template_constraints = {}
    templates: [DeclareTemplateModalDict] = []

    def __init__(self):
        super().__init__()
        self.events = {}
        self.attributes_list = {}
        self.template_constraints = {}
        self.templates = []
        self.update_props()

    def add_event(self, name: str, event_type: str) -> None:
        """
        Add an event to events dictionary if not exists yet.

        Parameters
        ----------
        name  the name of event or activity
        event_type  the type of the event, generally its "activity"

        Returns
        -------
        """

        event_name, event_type = (name, event_type)
        if event_name in self.events:
            raise KeyError(f"Multiple times the same activity [{event_name}] is declared")
        self.events[event_name] = DeclareModelEvent()
        self.events[event_name].name = event_name
        self.events[event_name].event_type = event_type

    def add_attribute(self, event_name: str, attr_name: str):
        f"""
        Add the bounded attribute to the event/activity

        Parameters
        ----------
        event_name: the name of event that for which the {attr_name} is bounded to.
        attr_name: attribute name
        Returns
        -------

        """
        if event_name not in self.events:
            raise ValueError(f"Unable to find the event or activity {event_name}")
        dme: DeclareModelEvent = self.events[event_name]
        attrs = dme.attributes
        if attrs is None:
            attrs = {}
            dme.attributes = attrs
        if attr_name in self.attributes_list:
            attrs[attr_name] = self.attributes_list[attr_name]  # saving the same reference. Same attr cannot have two values
        else:
            attrs[attr_name] = {"value": "", "value_type": ""}

        if attr_name not in self.attributes_list:
            # we save the reference of attributes in separate list
            # for improving computation
            self.attributes_list[attr_name] = attrs[attr_name]
            self.attributes_list[attr_name]["events_attached"] = [event_name]
        else:
            self.attributes_list[attr_name]["events_attached"].append(event_name)

    def add_attribute_value(self, attr_name: str, attr_type: DeclareModelAttributeType, attr_value: str):
        """
        Adding the attribute information
        Parameters
        ----------
        attr_name: str
        attr_type: DeclareModelAttributeType
        attr_value: str

        Returns
        -------
        """
        if attr_name not in self.attributes_list:
            raise ValueError(f"Unable to find attribute {attr_name}")
        attribute = self.attributes_list[attr_name]
        attribute["value"] = attr_value
        attribute["value_type"] = attr_type

    def add_template(self, line: str, template: Template, cardinality: str):
        templt = DeclareTemplateModalDict()
        self.templates.append(templt)
        templt.template = template
        templt.template_name = template.templ_str
        templt.template_line = line
        if template.supports_cardinality:
            templt.template_name += str(cardinality)
        compiler = re.compile(r"^(.*)\[(.*)\]\s*(.*)$")
        al = compiler.fullmatch(line)
        if al is None:
            return
        if len(al.group()) >= 2:
            events = al.group(2).strip().split(",")  # A, B
            events = [e.strip() for e in events]  # [A, B]
            templt.activities = events
        if len(al.group()) >= 3:
            conditions = al.group(3).strip()
            if len(conditions) == 0:
                return
            if len(conditions) > 1 and not conditions.startswith("|"):
                raise SyntaxError(f"Unable to parse template {template.templ_str}'s conditions."
                                  f" Conditions should start with \"|\"")
            templt.condition_line = conditions
            conditions = conditions.strip("|")
            conds_list = conditions.split("|")
            templt.condition = [cl.strip() for cl in conds_list]
            conds_len = len(conds_list)
            if conds_len > 3:
                raise ValueError(f"Unable to parse the line due to the exceeds conditions (> 3)")

    def update_props(self):
        """
        Updates the _dict, so it has updated values when any dict op is occurred
        Returns
        -------

        """
        self.key_value["events"] = self.events
        self.key_value["attributes_list"] = self.attributes_list
        self.key_value["template_constraints"] = self.template_constraints
        self.key_value["templates"] = self.templates

    def encode(self) -> DeclareParsedModel:
        return DeclareParsedModelEncoder().encode(self)


class DeclareParsedModelEncoder:
    encoded_dict = {}
    model: DeclareParsedModel

    def encode(self, dpm: DeclareParsedModel) -> DeclareParsedModel:
        # dpm: DeclareParsedModel = json.loads(dpm.to_json())  # TODO: check this. to void to get messed with reference/pointers
        dpm = copy.deepcopy(dpm)  # TODO: check this. to void to get messed with reference/pointers
        self.model = DeclareParsedModel()
        for event_name, event_obj in dpm.events.items():
            self.model.events[self.encode_event_name(event_name)] = event_obj
            for prop in event_obj:
                if prop == "name":
                    event_obj[prop] = self.encode_event_name(event_name)
                if prop == "event_type":
                    event_obj[prop] = self.encode_event_type(event_obj[prop])

        for attr_name, attr_obj in dpm.attributes_list.items():
            self.model.attributes_list[self.encode_event_name(attr_name)] = attr_obj
            if attr_obj["value_type"] is DeclareModelAttributeType.ENUMERATION:
                attr_obj["value"] = self.encode_enum_list(attr_obj["value"])
            if "events_attached" in attr_obj:
                attr_obj["events_attached"] = self.encode_str_list(attr_obj["events_attached"])

        for tmpl in dpm.templates:
            self.model.templates = tmpl
            if "activities" in tmpl:
                tmpl["activities"] = self.encode_str_list(tmpl["activities"])
            # compiler = re.compile(r"\"([\w,. ?]+)\"")
            compiler = re.compile(r"\"([\w,. ?]+)\"", re.MULTILINE)
            a, t, tm = tmpl.get_conditions()
            if a is not None:
                # c = DeclareParserUtility().parse_data_cond(a)
                c = self.parse_data_cond("A.grade > 10 and A.name in (x, y)  or A.grade < 3 and A.name in (z, v) ")
                print(c)
                out = compiler.findall(c)
                out.sort(key=lambda s: len(s))

                print(out)
                # print(len(out.groups()))
                # for groupNum in range(1, len(out.groups()) + 1):
                #     print(a, out.group(groupNum))
                    # groupNum = groupNum + 1
                # for matchNum, matched in enumerate(out, start=1):
                #     print(matchNum, matched)

            # TODO: template part conditions

        return self.model
        # pass

    def parse_data_cond(self, cond: str) -> str:
        try:
            cond = cond.strip()
            if cond == "":
                return cond
            py_cond, fill_enum_set = ("", False)
            conds = cond.split(" ")
            new_cond = []
            previous_char = ""
            counter = 0
            # while len(conds) > counter:
            #     c = conds[counter]
            #     if re.match(r'^[AaTt]\.', c):
            #         attr_name = c[2:]  # c = "A.grade"
            #         attr_name = self.encode_value(attr_name)
            #         nm = c[:2] + f"{attr_name}"
            #         conds.append(nm)
            #     elif c in ["and", "in", "or", "same", "different"] and previous_char is not "is":  # in case:
            #         previous_char = c
            #         continue
            #     # elif  c == "is":
            #
            #
            #     previous_char = c
            #         # con

            while cond:
                if cond.startswith("(") or cond.startswith(")"):
                    py_cond = py_cond + " " + cond[0]
                    cond = cond[1:].lstrip()
                    fill_enum_set = py_cond.endswith(" in (")
                else:
                    if not fill_enum_set:
                        s = re.split(r'[\s()]+', cond)
                        next_word = re.split(r'[\s()]+', cond)[0]
                        cond = cond[len(next_word):].lstrip()
                        if re.match(r'^[AaTt]\.', next_word):  # matches activation condition's A or target's T
                            py_cond = py_cond + " " + '"' + next_word[2:] + '" in ' + next_word[0] \
                                      + " and " + next_word[0] + '["' + next_word[2:] + '"]'
                        elif next_word.lower() == "is":
                            if cond.lower().startswith("not"):
                                cond = cond[3:].lstrip()
                                py_cond = py_cond + " !="
                            else:
                                py_cond = py_cond + " =="
                            tmp = []
                            while cond and not (cond.startswith(')') or cond.lower().startswith('and')
                                                or cond.lower().startswith('or')):
                                w = re.split(r'[\s()]+', cond)[0]
                                cond = cond[len(w):].lstrip()
                                tmp.append(w)
                            attr = " ".join(tmp)
                            py_cond += ' "' + attr + '"'
                        elif next_word == "=":
                            py_cond = py_cond + " =="
                        elif next_word.lower() == "and" or next_word.lower() == "or":
                            py_cond = py_cond + " " + next_word.lower()
                        elif next_word.lower() == "same":
                            tmp = []
                            while cond and not (cond.startswith(')') or cond.lower().startswith('and')
                                                or cond.lower().startswith('or')):
                                w = re.split(r'[\s()]+', cond)[0]
                                cond = cond[len(w):].lstrip()
                                tmp.append(w)
                            attr = " ".join(tmp)
                            py_cond = py_cond + " " + attr + " in A and " + attr + " in T " \
                                      + 'and A["' + attr + '"] == T["' + attr + '"]'
                        elif next_word.lower() == "different":
                            tmp = []
                            while cond and not (cond.startswith(')') or cond.lower().startswith('and')
                                                or cond.lower().startswith('or')):
                                w = re.split(r'[\s()]+', cond)[0]
                                cond = cond[len(w):].lstrip()
                                tmp.append(w)
                            attr = " ".join(tmp)
                            py_cond = py_cond + " " + attr + " in A and " + attr + " in T " \
                                      + 'and A["' + attr + '"] != T["' + attr + '"]'
                        elif next_word.lower() == "true":
                            py_cond = py_cond + " True"
                        elif next_word.lower() == "false":
                            py_cond = py_cond + " False"
                        else:
                            py_cond = py_cond + " " + next_word
                    else:
                        end_idx = cond.find(')')
                        enum_set = re.split(r',\s+', cond[:end_idx])
                        enum_set = [x.strip() for x in enum_set]
                        py_cond = py_cond + ' "' + '", "'.join(enum_set) + '"'
                        cond = cond[end_idx:].lstrip()

            return py_cond.strip()
        except Exception:
            raise SyntaxError

    def encode_event_name(self, s) -> str:
        return self.encode_value(s)

    def encode_event_type(self, s) -> str:
        return self.encode_value(s)

    def encode_enum_list(self, s) -> str:
        ss = s.split(",")
        ss = [self.encode_value(se) for se in ss]
        return ",".join(ss)

    def encode_str_list(self, lst: [str]) -> [str]:
        ss = [self.encode_value(se) for se in lst]
        return ss

    def encode_value(self, s) -> str:
        if s not in self.encoded_dict:
            # v = base64.b64encode(s.encode())
            # v = v.decode("utf-8")
            # v = v.decode("utf-8")
            v = hashlib.md5(s.encode()).hexdigest()
            self.encoded_dict[s] = v
        return self.encoded_dict[s]


class DeclModel(LTLModel):
    parsed_model: DeclareParsedModel

    def __init__(self):
        super().__init__()
        self.activities = []
        self.serialized_constraints = []
        self.constraints = []
        # self.parsed_model = DeclareParsedModel()

    def set_constraints(self):
        constraint_str = ''
        if len(self.constraints) > 0:
            for constraint in self.constraints:
                constraint_str = constraint['template'].templ_str
                if constraint['template'].supports_cardinality:
                    constraint_str += str(constraint['n'])
                constraint_str += '[' + ", ".join(constraint["activities"]) + '] |' + ' |'.join(constraint["condition"])
                self.serialized_constraints.append(constraint_str)

    def get_decl_model_constraints(self):
        return self.serialized_constraints

    def __str__(self):
        st = f"""{{"activities": {self.activities}, "serialized_constraints": {self.serialized_constraints},\
        "constraints": {self.constraints}, "parsed_model": {self.parsed_model.to_json()} }} """
        return st.replace("'", '"')
