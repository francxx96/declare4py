from enum import Enum


class Template(str, Enum):
    EXISTENCE = "Existence"
    ABSENCE = "Absence"
    EXACTLY = "Exactly"

    INIT = "Init"

    CHOICE = "Choice"
    EXCLUSIVE_CHOICE = "Exclusive Choice"

    RESPONDED_EXISTENCE = "Responded Existence"
    RESPONSE = "Response"
    ALTERNATE_RESPONSE = "Alternate Response"
    CHAIN_RESPONSE = "Chain Response"
    PRECEDENCE = "Precedence"
    ALTERNATE_PRECEDENCE = "Alternate Precedence"
    CHAIN_PRECEDENCE = "Chain Precedence"

    NOT_RESPONDED_EXISTENCE = "Not Responded Existence"
    NOT_RESPONSE = "Not Response"
    NOT_CHAIN_RESPONSE = "Not Chain Response"
    NOT_PRECEDENCE = "Not Precedence"
    NOT_CHAIN_PRECEDENCE = "Not Chain Precedence"

    @classmethod
    def get_template_from_string(cls, template_str):
        for t in Template:
            if t == template_str:
                return t
        return None

    @classmethod
    def get_unary_templates(cls):
        return [Template.ABSENCE, Template.EXACTLY, Template.EXISTENCE, Template.INIT]

    @classmethod
    def get_unary_templates_supporting_cardinality(cls):
        return [Template.ABSENCE, Template.EXACTLY, Template.EXISTENCE]

    @classmethod
    def get_unary_templates_not_supporting_cardinality(cls):
        return [Template.INIT]

    @classmethod
    def get_binary_templates(cls):
        return [Template.CHOICE, Template.EXCLUSIVE_CHOICE, Template.RESPONDED_EXISTENCE, Template.RESPONSE,
                Template.ALTERNATE_RESPONSE, Template.CHAIN_RESPONSE, Template.PRECEDENCE,
                Template.ALTERNATE_PRECEDENCE, Template.CHAIN_PRECEDENCE, Template.NOT_RESPONDED_EXISTENCE,
                Template.NOT_RESPONSE, Template.NOT_CHAIN_RESPONSE, Template.NOT_PRECEDENCE,
                Template.NOT_CHAIN_PRECEDENCE]


class TraceState(str, Enum):
    VIOLATED = "Violated"
    SATISFIED = "Satisfied"
    POSSIBLY_VIOLATED = "Possibly Violated"
    POSSIBLY_SATISFIED = "Possibly Satisfied"
