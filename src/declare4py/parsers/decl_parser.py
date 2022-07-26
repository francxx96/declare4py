from ..enums import Template
from ..models import DeclModel
import re


def parse_data_cond(cond):
    try:
        cond = cond.strip()
        if cond == "":
            return "True"

        # List containing translations from decl format to python
        py_cond = ""
        fill_enum_set = False

        while cond:
            if cond.startswith("(") or cond.startswith(")"):
                py_cond = py_cond + " " + cond[0]
                cond = cond[1:].lstrip()
                fill_enum_set = py_cond.endswith(" in (")

            else:
                if not fill_enum_set:
                    next_word = re.split(r'[\s()]+', cond)[0]
                    cond = cond[len(next_word):].lstrip()

                    if re.match(r'^[AaTt]\.', next_word):
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


def parse_time_cond(condition):
    try:
        if condition.strip() == "":
            condition = "True"
            return condition

        if re.split(r'\s*,\s*', condition.strip())[2].lower() == "s":
            time_measure = "seconds"
        elif re.split(r'\s*,\s*', condition.strip())[2].lower() == "m":
            time_measure = "minutes"
        elif re.split(r'\s*,\s*', condition.strip())[2].lower() == "h":
            time_measure = "hours"
        elif re.split(r'\s*,\s*', condition.strip())[2].lower() == "d":
            time_measure = "days"
        else:
            time_measure = None

        min_td = "timedelta(" + time_measure + "=float(" + str(condition.split(",")[0]) + "))"
        max_td = "timedelta(" + time_measure + "=float(" + str(condition.split(",")[1]) + "))"

        condition = min_td + ' <= abs(A["time:timestamp"] - T["time:timestamp"]) <= ' + max_td
        return condition

    except Exception:
        raise SyntaxError


def parse_decl_from_file(path):
    fo = open(path, "r+")
    lines = fo.readlines()
    fo.close()
    return parse_decl(lines)


def parse_decl_from_string(decl_string):
    return parse_decl(decl_string.split("\n"))


def parse_decl(lines):
    result = DeclModel()

    for line in lines:
        line = line.strip()

        split = line.split(maxsplit=1)
        if split[0].strip() == 'activity':
            result.activities.append(split[1].strip())
            continue

        split = line.split("[", 1)
        template_search = re.search(r'(^.+?)(\d*$)', split[0])

        if template_search is not None:
            template_str, cardinality = template_search.groups()
            template = Template.get_template_from_string(template_str)

            if template is not None:
                attributes = split[1].split("]")[0]
                tmp = {
                    "template": template,
                    "attributes": attributes,
                    "condition": re.split(r'\s+\|', line)[1:]
                }

                if template.supports_cardinality:
                    tmp['n'] = 1 if not cardinality else int(cardinality)

                result.checkers.append(tmp)

    result.set_constraints()
    return result
