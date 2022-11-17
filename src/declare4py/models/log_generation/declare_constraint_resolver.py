from __future__ import annotations

import re
import typing
import boolean

from src.declare4py.models.log_generation.declare_model import ConstraintTemplates, DeclareEventValueType

# class ConstrainTemplates:
CONSTRAINTS_TEMPLATES = {

    "Init": {
        "binary": False, "negative": False, "cardinality": False,
        "semantic": "First task is A"
    },

    "Existence": {
        "binary": False, "negative": False, "cardinality": True,
        "semantic": "Task A should be executed. If cardinality defined, should be executed n or more times."
    },
    "Absence": {
        "binary": False, "negative": False, "cardinality": True,
        "semantic": "Task A should not be executed. If cardinality defined, should be executed n times or less"
    },
    "Exactly": {
        "binary": False, "negative": False, "cardinality": True,
        "semantic": "Task A should be executed (exactly) N times"
    },

    "Choice": {"binary": True, "negative": False, "cardinality": False,
               "semantic": "Task A or task B should be executed (or both)"},
    "ExclusiveChoice": {"binary": True, "negative": False, "cardinality": False,
                        "semantic": "Task A or task B should be executed, but not both"},
    "RespondedExistence": {"binary": True, "negative": False, "cardinality": False,
                           "semantic": "If task A executed, task B executed as well"},
    "Response": {"binary": True, "negative": False, "cardinality": False,
                 "semantic": "If task A executed, task B executed after A"},
    "AlternateResponse": {"binary": True, "negative": False, "cardinality": False,
                          "semantic": "If task A executed, task B executed after A, without other A in between "},
    "ChainResponse": {"binary": True, "negative": False, "cardinality": False,
                      "semantic": "If task A executed, task B executed next"},
    "Precedence": {"binary": True, "negative": False, "cardinality": False,
                   "semantic": "If task A executed, task B was executed before A"},
    "AlternatePrecedence": {"binary": True, "negative": False, "cardinality": False,
                            "semantic": "If task A executed, task B was executed before A, without other A in between"},
    "CoExistence": {"binary": True, "negative": False, "cardinality": False, "semantic": "...."},
    "NotCoExistence": {"binary": True, "negative": True, "cardinality": False, "semantic": "...."},
    "ChainPrecedence": {"binary": True, "negative": False, "cardinality": False,
                        "semantic": "If task A executed, previous executed task was B"},

    "NotRespondedExistence": {"binary": True, "negative": True, "cardinality": False,
                              "semantic": "If task A executed, task B is not executed"},
    "NotResponse": {"binary": True, "negative": True, "cardinality": False,
                    "semantic": "If task A executed, task B will not be executed after A"},
    "NotPrecedence": {"binary": True, "negative": True, "cardinality": False,
                      "semantic": "If task A executed, task B was not executed before A"},
    "NotChainResponse": {"binary": True, "negative": True, "cardinality": False,
                         "semantic": "If task A executed, task B is not executed next"},
    "NotChainPrecedence": {"binary": True, "negative": True, "cardinality": False,
                           "semantic": "If task A executed, previous executed task was not B"},
}


class DeclareConstraintConditionResolver:

    def resolve_to_asp(self, ct: ConstraintTemplates, attrs: dict, idx: int = 0):
        ls = []
        if ct.active_cond:
            ls.append('activation({},{}).'.format(idx, ct.events_list[0].lower()))
            exp, n2c, c2n = self.parsed_condition('activation', ct.active_cond)
            conditions = set(n2c.keys())
            if exp.isliteral:
                ls.append('activation_condition({},T):- {}({},T).'.format(idx, str(exp), idx))
            s = self.tree_conditions_to_asp("activation", exp, "activation_condition", idx, conditions)
            if s and len(s) > 0:
                ls = ls + s
            for n, c in n2c.items():
                s = self.condition_to_asp(n, c, idx, attrs)
                if s and len(s) > 0:
                    ls = ls + s
        if ct.correlation_cond:
            ls.append("")
            target = ct.events_list[1]
            ls.append('target({},{}).'.format(idx, target.lower()))
            exp, n2c, c2n = self.parsed_condition('correlation', ct.correlation_cond)
            conditions = set(n2c.keys())
            if exp.isliteral:
                ls.append('correlation_condition({},T):- {}({},T).'.format(idx, str(exp), idx))
            s = self.tree_conditions_to_asp("correlation", exp, "correlation_condition", idx, conditions)
            if s and len(s) > 0:
                ls = ls + s
            for n, c in n2c.items():
                s = self.condition_to_asp(n, c, idx, attrs)
                if s and len(s) > 0:
                    ls = ls + s
        return ls

    def condition_to_asp(self, name, cond, i, attrs):
        name = name + '({},T)'.format(i)
        string = re.sub('is not', 'is_not', cond)
        string = re.sub('not in', 'not_in', string)
        if cond.__contains__("."):
            attr = cond.split(".")[1].strip()  # A.grade>2
        else:
            attr = cond
        attr = re.search('[\w]+', attr)
        ls = []
        if attr:
            attr = attr.group(0).strip()
            if attr not in attrs:
                raise ValueError(f"Unable to find the attribute \"{attr}\" in condition \"{cond}\". name: \"{name}\"")
            attr_obj = attrs[attr][0]
            if attr_obj.typ == DeclareEventValueType.ENUMERATION:  # ["is_range_typ"]:  # Enumeration
                cond_type = cond.split(' ')[1]
                if cond_type == 'is':
                    s = 'assigned_value({},{},T)'.format(attr, string.split(' ')[2])
                    ls.append('{} :- {}.'.format(name, s))
                elif cond_type == 'is_not':
                    s = 'time(T), not assigned_value({},{},T)'.format(attr, string.split(' ')[2])
                    ls.append('{} :- {}.'.format(name, s))
                elif cond_type == 'in':
                    for value in string.split(' ')[2][1:-1].split(','):
                        asp_cond = 'assigned_value({},{},T)'.format(attr, value)
                        ls.append('{} :- {}.'.format(name, asp_cond))
                else:
                    asp_cond = 'time(T),'
                    for value in cond.split(' ')[2][1:-1].split(','):
                        asp_cond = asp_cond + 'not assigned_value({},{},T),'.format(attr, value)
                    asp_cond = asp_cond[:-1]
                    ls.append('{} :- {}.'.format(name, asp_cond))
            elif attr_obj.typ == DeclareEventValueType.INTEGER:
                relations = ['<=', '>=', '=', '<', '>']
                for rel in relations:
                    if rel in cond:
                        value = string.split(rel)[1]
                        ls.append('{} :- assigned_value({},V,T),V{}{}.'.format(name, attr, rel, value))
                        break
        return ls

    def parsed_condition(self, condition: typing.Literal['activation', 'correlation'], string: str):
        string = re.sub('\)', ' ) ', string)
        string = re.sub('\(', ' ( ', string)
        string = string.strip()
        string = re.sub(' +', ' ', string)
        string = re.sub('is not', 'is_not', string)
        string = re.sub('not in', 'not_in', string)
        string = re.sub(' *> *', '>', string)
        string = re.sub(' *< *', '<', string)
        string = re.sub(' *= *', '=', string)
        string = re.sub(' *<= *', '<=', string)
        string = re.sub(' *>= *', '>=', string)
        form_list = string.split(" ")

        for i in range(len(form_list) - 1, -1, -1):
            el = form_list[i]
            if el == 'in' or el == 'not_in':
                end_index = form_list[i:].index(')')
                start_index = i - 1
                end_index = end_index + i + 1
                form_list[start_index:end_index] = [' '.join(form_list[start_index:end_index])]
            elif el == 'is' or el == 'is_not':
                start_index = i - 1
                end_index = i + 2
                form_list[start_index:end_index] = [' '.join(form_list[start_index:end_index])]

        for i in range(len(form_list)):
            el = form_list[i]
            if '(' in el and ')' in el:
                el = re.sub('\( ', '(', el)
                el = re.sub(', ', ',', el)
                el = re.sub(' \)', ')', el)
                form_list[i] = el

        keywords = {'and', 'or', '(', ')'}
        c = 0
        name_to_cond = dict()
        cond_to_name = dict()
        for el in form_list:
            if el not in keywords:
                c = c + 1
                name_to_cond[condition + '_condition_' + str(c)] = el
                cond_to_name[el] = condition + '_condition_' + str(c)
        form_string = ''
        for el in form_list:
            if el in cond_to_name:
                form_string = form_string + cond_to_name[el] + ' '
            else:
                form_string = form_string + el + ' '

        algebra = boolean.BooleanAlgebra()
        expression = algebra.parse(form_string, simplify=True)
        return expression, name_to_cond, cond_to_name

    def tree_conditions_to_asp(self, condition: typing.Literal['activation', 'correlation'],
                               expression, cond_name: str, i, conditions_names,
                               lp_st=None) -> typing.List[str] | None:
        if lp_st is None:
            lp_st = []
        def expression_to_name(expression):
            if expression.isliteral:
                condition_name = str(expression)
            else:
                condition_name = condition + '_condition_' + ''.join(
                    [str(symbol).split('_')[2] for symbol in expression.get_symbols()])
                while condition_name in conditions_names:
                    condition_name = condition_name + '_'
                conditions_names.add(condition_name)
            return condition_name + '({},T)'.format(i)

        def no_params(arg_name):
            return arg_name.split('(')[0]

        if expression.isliteral:
            return
        cond_name = cond_name + '({},T)'.format(i)
        formula_type = expression.operator
        formula_args = expression.args
        if formula_type == '|':
            for arg in formula_args:
                arg_name = expression_to_name(arg)
                lp_st.append('{} :- {}.'.format(cond_name, arg_name))
                self.tree_conditions_to_asp(condition, arg, no_params(arg_name), i, conditions_names, lp_st)
        if formula_type == '&':
            args_name = ''
            for arg in formula_args:
                arg_name = expression_to_name(arg)
            args_name = args_name[:-1]  # remove last comma
            lp_st.append('{} :- {}.'.format(cond_name, args_name))
            for arg in formula_args:  # breadth-first (è più costoso della depth ma è più elegante, è la stessa della disgiunzione)
                arg_name = expression_to_name(arg)
                self.tree_conditions_to_asp(condition, arg, no_params(arg_name), i, lp_st)
        return lp_st


class DeclareConstraintResolver:
    CONSTRAINTS_TEMPLATES_PATTERN = "^(.*)\[(.*)\]\s*(.*)$"

    def __init__(self):
        self.templates_name = CONSTRAINTS_TEMPLATES.keys()

    def parse_template(self, line) -> None | ConstraintTemplates:
        compiler = re.compile(self.CONSTRAINTS_TEMPLATES_PATTERN)
        al = compiler.fullmatch(line)
        if al is None:
            return
        tmp_name = al.group(1).replace(" ", "").strip()  # template names: Response, Existence...
        tmp_name = tmp_name.replace("-", "").strip()  # template names: Co-Existence...
        if tmp_name not in self.templates_name:
            raise ValueError(f"Constraint template {tmp_name} is not supported!")
        events = al.group(2).strip().split(",")  # A, B
        events = [e.strip() for e in events]  # [A, B]
        conditions = al.group(3)  # |A.grade > 2 and A.name in (x, y) or A.grade < 2 and A.name in (z, v) |B.grade > 5 |1,5,s
        ct = ConstraintTemplates()
        ct.template_name = str(tmp_name)
        ct.events_list = events
        ct.conditions = str(conditions)
        self.__parse_constraint_conditions(conditions, ct)
        return ct

    def __parse_constraint_conditions(self, conditions_part: str, ct_model: ConstraintTemplates):
        conds_list = conditions_part.strip().strip("|").split("|")
        conds_len = len(conds_list)
        if conds_len >= 1:
            active = conds_list[0].strip()
            if active and len(active) > 0:
                ct_model.active_cond = active
        if conds_len >= 2:
            correlated = conds_list[1].strip()
            if correlated and len(correlated) > 0:
                ct_model.correlation_cond = correlated
        if conds_len == 3:
            time = conds_list[2].strip()
            if time and len(time) > 0:
                ct_model.ts = time
        if conds_len > 3:  # TODO: what to in this case
            raise ValueError(f"Unable to parse the line due to the exceeds conditions (> 3)")
        return ct_model


