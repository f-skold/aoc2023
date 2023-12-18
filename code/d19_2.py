import copy
from typing import List

import common


class RulesEngine:
    def __init__(self, input, debug=False):
        self.rules = {}
        self.items = []
        self._debug = debug
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
                if debug:
                    print(f"R: {name} => {self.rules[name]}")
            else:
                # item
                ratings = {}
                ratings1 = row1[1:-1].split(",")
                for rating in ratings1:
                    temp2 = rating.split("=")

                    ratings[temp2[0]] = int(temp2[1])
                if debug:
                    print(ratings)
                self.items.append(ratings)

    @common.timing
    def solve(self, game_b=False) -> int:
        ranges = {}
        for char in ["x", "m", "a", "s"]:
            ranges[char] = [1, 4000]

        results = self.do_try("in", ranges)
        print(results)
        return results

    def do_try(self, workflow_name, ranges):
        if self._debug:
            print(f"do_try: {ranges}, name={workflow_name}")
        if "A" == workflow_name:
            product = 1
            for range1 in ranges.values():
                product *= range1[1] - range1[0] + 1
            if self._debug:
                print(f"A: {ranges} => {product}")
            return product

        results = 0
        if workflow_name not in ["A", "R"]:
            rules = self.rules[workflow_name]
            for rule in rules:
                if 1 == len(rule):
                    next_workflow_name = rule[0]
                    return results + self.do_try(next_workflow_name, ranges)
                else:
                    variable = rule[0]
                    range1 = ranges[variable]
                    threshold = rule[2]
                    candidate_workflow_name = rule[3]
                    if ">" == rule[1]:
                        if range1[0] > threshold:
                            return results + self.do_try(candidate_workflow_name, ranges)
                        elif range1[1] < threshold:
                            pass
                        else:
                            ranges2 = copy.deepcopy(ranges)
                            ranges2[variable] = [threshold + 1, range1[1]]
                            results += self.do_try(candidate_workflow_name, ranges2)
                            ranges[variable] = [range1[0], threshold]
                    elif "<" == rule[1]:
                        if range1[1] < threshold:
                            return results + self.do_try(candidate_workflow_name, ranges)
                            break
                        elif range1[0] > threshold:
                            pass
                        else:
                            ranges3 = copy.deepcopy(ranges)
                            ranges3[variable] = [range1[0], threshold - 1]
                            results += self.do_try(candidate_workflow_name, ranges3)

                            ranges[variable] = [threshold, range1[1]]

        if "A" == workflow_name:
            product = 1
            for range1 in ranges.values():
                product *= range1[1] - range1[0]
            print(f"A second: {ranges} => {product}")
            results += product
        return results


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
            print(f"Difference, expected={expected}, actual={sum}, diff={expected - sum}")
            print(f"{expected} <= expected")
            print(f"{sum} <= actual")

    return sum


res = run("test_19.txt", expected=167409079868000)
print()
res = run("data_19.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
