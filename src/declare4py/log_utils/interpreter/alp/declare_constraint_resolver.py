from __future__ import annotations

import re
import typing
import boolean

from src.declare4py.log_utils.parsers.declare.decl_model import DeclareTemplateModalDict, DeclareModelAttributeType


class DeclareModalConstraintConditionResolver:

    def resolve_to_asp(self, ct: DeclareTemplateModalDict, attrs: dict, idx: int = 0):
        ls = []
        activation, target_cond, time = ct.get_conditions()
        if activation:
            ls.append('activation({},{}).'.format(idx, ct.activities[0].lower()))
            exp, n2c, c2n = self.parsed_condition('activation', activation)
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
        if target_cond:
            target = ct.activities[1]
            ls.append('target({},{}).'.format(idx, target.lower()))
            exp, n2c, c2n = self.parsed_condition('correlation', target_cond)
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
        attr = re.search(r'\w+', attr)
        ls = []
        if attr:
            attr = attr.group(0).strip()
            if attr not in attrs:
                raise ValueError(f"Unable to find the attribute \"{attr}\" in condition \"{cond}\". name: \"{name}\"")
            attr_obj = attrs[attr]
            value_typ = attr_obj["value_type"]
            if value_typ == DeclareModelAttributeType.ENUMERATION:  # ["is_range_typ"]:  # Enumeration
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
            elif value_typ == DeclareModelAttributeType.INTEGER or value_typ == DeclareModelAttributeType.FLOAT or \
                    value_typ == DeclareModelAttributeType.INTEGER_RANGE or \
                    value_typ == DeclareModelAttributeType.FLOAT_RANGE:
                relations = ['<=', '>=', '=', '<', '>']
                for rel in relations:
                    if rel in cond:
                        value = string.split(rel)[1]
                        ls.append('{} :- assigned_value({},V,T),V{}{}.'.format(name, attr, rel, value))
                        break
        return ls

    def parsed_condition(self, condition: typing.Literal['activation', 'correlation'], string: str):
        string = re.sub(r'\)', ' ) ', string)
        string = re.sub(r'\(', ' ( ', string)
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
                el = re.sub(r'\( ', '(', el)
                el = re.sub(', ', ',', el)
                el = re.sub(r' \)', ')', el)
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
            for arg in formula_args:
                arg_name = expression_to_name(arg)
                self.tree_conditions_to_asp(condition, arg, no_params(arg_name), i, lp_st)
        return lp_st

