import json
from enum import Enum

from src.declare4py.log_utils.ltl_model import LTLModel


class DeclareModelEvent(dict):
    name: str
    event_type: str
    attribute: dict[str, dict]

    def __init__(self, *args, **kw):
        super().__init__()
        self._dict = dict(*args, **kw)
        self.attribute = {}
        self._dict["attribute"] = self.attribute

    def __getitem__(self, key):
        self.update_props()
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __iter__(self):
        self.update_props()
        return iter(self._dict)

    def __len__(self):
        self.update_props()
        return len(self._dict)

    def __delitem__(self, key):
        self.update_props()
        self._dict["name"] = self.name
        self._dict["event_type"] = self.event_type
        self._dict["attribute"] = self.attribute
        del self._dict[key]

    def __str__(self):
        self.update_props()
        return str(self._dict)

    def __repr__(self):
        self.update_props()
        return str(self._dict)

    def update_props(self):
        self._dict["name"] = self.name
        self._dict["event_type"] = self.event_type
        self._dict["attribute"] = self.attribute


class DeclareModelAttributeType(str, Enum):
    INTEGER = "integer"
    FLOAT = "float"
    INTEGER_RANGE = "integer_range"
    FLOAT_RANGE = "float_range"
    ENUMERATION = "enumeration"


class DeclareParsedModel(dict):
    events: {str: DeclareModelEvent} = {}
    attributes_list: dict[str, dict] = []
    template_constraints = {}

    def __init__(self, *args, **kw):
        super().__init__()
        self._dict = dict(*args, **kw)
        self.events = {}
        self.attributes_list = {}
        self.template_constraints = {}
        self.__update_dict()

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
        attrs = dme.attribute
        if attrs is None:
            attrs = {}
            dme.attribute = attrs
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

    def __update_dict(self):
        """
        Updates the _dict, so it has updated values when any dict op is occurred
        Returns
        -------

        """
        self._dict["events"] = self.events
        self._dict["attributes_list"] = self.attributes_list
        self._dict["template_constraints"] = self.template_constraints

    def __getitem__(self, key):
        self.__update_dict()
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __iter__(self):
        self.__update_dict()
        return iter(self._dict)

    def __len__(self):
        self.__update_dict()
        return len(self._dict)

    def __delitem__(self, key):
        self.__update_dict()
        del self._dict[key]

    def __str__(self):
        self.__update_dict()
        return json.dumps(self._dict)

    def __repr__(self):
        self.__update_dict()
        return self.__str__()


class DeclModel(LTLModel):
    parsed_model: DeclareParsedModel

    def __init__(self):
        super().__init__()
        self.activities = []
        self.serialized_constraints = []
        self.constraints = []
        self.parsed_mode = {}

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
