from _future_ import annotations

from enum import Enum


class Template(str, Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = str.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, templ_str: str, is_binary: bool, is_negative: bool, supports_cardinality: bool):
        self.templ_str = templ_str
        self.is_binary = is_binary
        self.is_negative = is_negative
        self.supports_cardinality = supports_cardinality

    EXISTENCE = "Existence", False, False, True
    ABSENCE = "Absence", False, False, True
    EXACTLY = "Exactly", False, False, True

    INIT = "Init", False, False, False

    CHOICE = "Choice", True, False, False
    EXCLUSIVE_CHOICE = "Exclusive Choice", True, False, False
    RESPONDED_EXISTENCE = "Responded Existence", True, False, False
    RESPONSE = "Response", True, False, False
    ALTERNATE_RESPONSE = "Alternate Response", True, False, False
    CHAIN_RESPONSE = "Chain Response", True, False, False
    PRECEDENCE = "Precedence", True, False, False
    ALTERNATE_PRECEDENCE = "Alternate Precedence", True, False, False
    CHAIN_PRECEDENCE = "Chain Precedence", True, False, False

    NOT_RESPONDED_EXISTENCE = "Not Responded Existence", True, True, False
    NOT_RESPONSE = "Not Response", True, True, False
    NOT_CHAIN_RESPONSE = "Not Chain Response", True, True, False
    NOT_PRECEDENCE = "Not Precedence", True, True, False
    NOT_CHAIN_PRECEDENCE = "Not Chain Precedence", True, True, False

    @classmethod
    def get_template_from_string(cls, template_str):
        return next(filter(lambda t: t.templ_str == template_str, Template), None)

    @classmethod
    def get_unary_templates(cls):
        return tuple(filter(lambda t: not t.is_binary, Template))

    @classmethod
    def get_binary_templates(cls):
        return tuple(filter(lambda t: t.is_binary, Template))

    @classmethod
    def get_positive_templates(cls):
        return tuple(filter(lambda t: not t.is_negative, Template))

    @classmethod
    def get_negative_templates(cls):
        return tuple(filter(lambda t: t.is_negative, Template))

    def __str__(self):
        return "<Template." + str(self.templ_str) + ": " + str(self.value) + " >"

    def __repr__(self):
        return "\""+str(self.__str__())+"\""


class TraceState(str, Enum):
    VIOLATED = "Violated"
    SATISFIED = "Satisfied"
    POSSIBLY_VIOLATED = "Possibly Violated"
    POSSIBLY_SATISFIED = "Possibly Satisfied"
