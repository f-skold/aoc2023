from typing import List

import common


class RulesEngine:
    def __init__(self, input):
        self.rules = {}
        self.items = []
        state = 0
        for row in input:
            row1 = row.strip()
            if 0 == len(row1):
                state = 1
            elif 0 == state:
                # rule
                temp = row1.split("{")
                name = temp[0]
                rules = temp[1][:-1]
                rules2 = rules.split(",")
                list_of_rules = []
                for rule2 in rules2:
                    parts = rule2.split(":")
                    if len(parts) == 1:
                        list_of_rules.append(parts)
                    else:
                        temp1 = parts[0].split("<")
                        if len(temp1) == 2:
                            list_of_rules.append([temp1[0], "<", int(temp1[1])])
                        else:
                            temp2 = parts[0].split(">")
                            if len(temp2) == 2:
                                list_of_rules.append([temp2[0], ">", int(temp2[1])])
                            else:
                                raise Exception(f"Not splitted: {parts[0]}")
                        list_of_rules[-1].append(parts[1])

                self.rules[name] = list_of_rules
                # print(f"R: {name} => {self.rules[name]}")
            else:
                # item
                ratings = {}
                ratings1 = row1[1:-1].split(",")
                for rating in ratings1:
                    temp2 = rating.split("=")

                    ratings[temp2[0]] = int(temp2[1])
                # print(ratings)
                self.items.append(ratings)

    def solve(self, game_b=False) -> int:
        sum1 = 0
        for item in self.items:
            visited_rules = []
            workflow_name = "in"
            while workflow_name not in ["A", "R"]:
                visited_rules.append(workflow_name)

                rules = self.rules[workflow_name]
                for rule in rules:
                    if 1 == len(rule):
                        workflow_name = rule[0]
                        break
                    else:
                        value = item[rule[0]]
                        if ">" == rule[1]:
                            if value > rule[2]:
                                workflow_name = rule[3]
                                break
                        elif "<" == rule[1]:
                            if value < rule[2]:
                                workflow_name = rule[3]
                                break
            if "A" == workflow_name:
                sum1 += sum(item.values())
        return sum1


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum = 0

    instance = RulesEngine(input)
    sum = instance.solve()

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Difference, expected={expected}, actual={sum}")
    return sum


res = run("test_19.txt", expected=19114)
print()
res = run("data_19.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
