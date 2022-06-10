from src.enums import Template
from src.models import DeclModel
import re


def parse_data_cond(cond):
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

                    attr = re.split(r'[\s()]+', cond)[0]
                    cond = cond[len(attr):].lstrip()

                    py_cond = py_cond + ' "' + attr + '"'

                elif next_word == "=":
                    py_cond = py_cond + " =="

                elif next_word.lower() == "and" or next_word.lower() == "or":
                    py_cond = py_cond + " " + next_word.lower()

                elif next_word.lower() == "same":
                    attr = re.split(r'[\s()]+', cond)[0]
                    cond = cond[len(attr):].lstrip()

                    py_cond = py_cond + " " + attr + " in A and " + attr + " in T " \
                              + 'and A["' + attr + '"] == T["' + attr + '"]'

                elif next_word.lower() == "different":
                    attr = re.split(r'[\s()]+', cond)[0]
                    cond = cond[len(attr):].lstrip()

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


def parse_temporal_cond(condition):
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


def parse_decl(path):
    fo = open(path, "r+")
    lines = fo.readlines()
    result = DeclModel()

    for line in lines:
        if line.startswith('activity'):
            result.activities.append(line.split()[1])

        elif line.startswith(tuple(map(lambda c: c.value, Template))):
            split = line.split("[")
            key = split[0].strip()
            attribute = split[1].split("]")[0]

            tmp = {"key": key, "attribute": attribute}

            if (line.startswith(Template.EXISTENCE)
                    or line.startswith(Template.ABSENCE)
                    or line.startswith(Template.EXACTLY)):

                n = 1 if not any(map(str.isdigit, key)) else int(re.search(r'\d+', key).group())

                tmp['condition'] = [line.split("|")[1], n, line.split("|")[-1]]
                result.checkers.append(tmp)

            elif line.startswith(Template.INIT):

                tmp['condition'] = [line.split("|")[1]]
                result.checkers.append(tmp)

            elif (line.startswith(Template.CHOICE)
                  or line.startswith(Template.EXCLUSIVE_CHOICE)):

                tmp['condition'] = [line.split("|")[1], line.split("|")[-1]]
                result.checkers.append(tmp)

            elif (line.startswith(Template.RESPONDED_EXISTENCE)
                  or line.startswith(Template.RESPONSE)
                  or line.startswith(Template.ALTERNATE_RESPONSE)
                  or line.startswith(Template.CHAIN_RESPONSE)
                  or line.startswith(Template.PRECEDENCE)
                  or line.startswith(Template.ALTERNATE_PRECEDENCE)
                  or line.startswith(Template.CHAIN_PRECEDENCE)
                  or line.startswith(Template.NOT_RESPONDED_EXISTENCE)
                  or line.startswith(Template.NOT_RESPONSE)
                  or line.startswith(Template.NOT_CHAIN_RESPONSE)
                  or line.startswith(Template.NOT_PRECEDENCE)
                  or line.startswith(Template.NOT_CHAIN_PRECEDENCE)):

                tmp['condition'] = [line.split("|")[1], line.split("|")[2], line.split("|")[-1]]
                result.checkers.append(tmp)

    fo.close()
    return result
