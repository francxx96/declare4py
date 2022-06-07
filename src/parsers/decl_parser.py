from src.enums import Template
from src.models import DeclModel
import re


def modify_condition(condition):
    if condition.strip() == "":
        condition = "True"
        return condition

    if "is" in condition:
        condition = condition.replace("is", "==")

    words = condition.split()

    for index, word in enumerate(words):
        if "A." in word:
            words[index] = 'A["' + word[2:] + '"]'
            if not words[index + 2].isdigit():
                words[index + 2] = '"' + words[index + 2] + '"'

        elif "T." in word:
            words[index] = 'T["' + word[2:] + '"]'
            if not words[index + 2].isdigit():
                words[index + 2] = '"' + words[index + 2] + '"'

        elif word == "same":
            words[index] = 'A["' + words[index + 1] + '"] == T["' + words[index + 1] + '"]'
            words[index + 1] = ""

    words = list(filter(lambda word : word != "", words))
    condition = " ".join(words)
    return condition


def modify_temporal_condition(condition):
    if condition.strip() == "":
        condition = "True"
        return condition

    if condition.strip().split(",")[2] == "s":
        time_measure = "seconds"
    elif condition.strip().split(",")[2] == "m":
        time_measure = "minutes"
    elif condition.strip().split(",")[2] == "h":
        time_measure = "hours"
    elif condition.strip().split(",")[2] == "d":
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

                tmp['condition'] = [modify_condition(line.split("|")[1]),
                                    n,
                                    modify_temporal_condition(line.split("|")[-1])]
                result.checkers.append(tmp)

            elif line.startswith(Template.INIT):

                tmp['condition'] = [modify_condition(line.split("|")[1])]
                result.checkers.append(tmp)

            elif (line.startswith(Template.CHOICE)
                  or line.startswith(Template.EXCLUSIVE_CHOICE)):

                tmp['condition'] = [modify_condition(line.split("|")[1]),
                                    modify_temporal_condition(line.split("|")[-1])]
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

                tmp['condition'] = [modify_condition(line.split("|")[1]),
                                    modify_condition(line.split("|")[2]),
                                    modify_temporal_condition(line.split("|")[-1])]
                result.checkers.append(tmp)

    fo.close()
    return result
