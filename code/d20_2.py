import math
import collections
from enum import Enum
from typing import List

import common

OP = 0
DEST = 1


class Operation(Enum):
    NO_OP = 0
    FLIP_FLOP = 1
    CONJUNCTION = 2


class PulseTrain:
    def __init__(self, input, debug=True):
        self._debug = debug
        modules = {}
        conjunctions1 = []
        conjunctions2 = collections.defaultdict(dict)
        self.flips = collections.defaultdict(int)
        self.debug("== Modules")
        rx = None
        for row in input:
            parts1 = row.strip().split("->")
            name = parts1[0].strip()
            destinations = parts1[1].strip().split(",")
            op = Operation.NO_OP
            if "%" == name[0]:
                op = Operation.FLIP_FLOP
                name = name[1:]
            elif "&" == name[0]:
                op = Operation.CONJUNCTION
                name = name[1:]
                conjunctions1.append(name)
                conjunctions2[name]
            dests = [d.strip() for d in destinations]
            modules[name] = (op, dests)
            if "rx" in dests:
                rx = name
            self.debug(f"{name} -> {modules[name]}")
        self.modules = modules
        for key, value in modules.items():
            for dest in value[DEST]:
                if dest in conjunctions1:
                    conjunctions2[dest][key] = 0
        self.conjunction_inputs = conjunctions2
        self.rx_inputs = {key: 0 for key in self.conjunction_inputs[rx].keys()}
        self.presses = 0
        self.count = [0, 0]
        self.queue = []
        self.unknows = []
        self.reset()

    def reset(self):
        self.count = [0, 0]
        self.flips = collections.defaultdict(int)

    def debug(self, message: str):
        if self._debug:
            print(message)

    def enqueue(self, from1: str, dest: str, signal: int):
        # for index, value in enumerate(self.queue):
        #     if value[0] == dest:
        #         self.queue[index] = (dest, signal)
        #         return
        self.queue.append((from1, dest, signal))
        # self.count[signal] += 1

    def push(self):
        self.presses += 1
        signal = 0
        key = "broadcaster"
        self.queue.append((None, key, signal))
        if all(self.rx_inputs.values()):
            result = math.prod(self.rx_inputs.values())
            print(f"result: {result}")
            return result

        while len(self.queue) > 0:
            from1, key, in_signal = self.queue.pop(0)
            self.count[in_signal] += 1
            # self.debug(f"Injecting, {from1} {key}, {in_signal}")
            signal = in_signal
            if key not in self.modules:
                if key not in self.unknows:
                    self.unknows.append(key)
                    print(f"Unknown port: {key}")
                continue
            module = self.modules[key]
            op = module[OP]
            if Operation.NO_OP == op:
                signal = in_signal
            elif Operation.CONJUNCTION == op:
                self.conjunction_inputs[key][from1] = in_signal
                # check all inputs
                input_states = self.conjunction_inputs[key].values()
                signal = not all(input_states)

                if "rx" in module[DEST]:
                    for source, value in self.conjunction_inputs[key].items():
                        if value:
                            self.rx_inputs[source] = self.presses
                            print(f"rx_inputs set: {self.presses}, ({from1}), {source}, {value}")
                # not remembered
            elif Operation.FLIP_FLOP == op:
                if 0 == in_signal:
                    signal = not self.flips[key]
                    self.flips[key] = signal
                else:
                    continue
            else:
                print(f"Unknown operation: {op}")

            for d in module[DEST]:
                # self.debug(f"{key} -{signal}-> {d}")
                self.enqueue(key, d, signal)

        return False

    def solve(self, game_b=False) -> int:
        print("Rx inputs: ", ", ".join(self.rx_inputs.keys()))
        while True:
            # self.debug(f"== Push {i}")
            result = self.push()
            if result:
                break
        print(f"solve: count={self.count}")
        # return self.count[0] * self.count[1] * 1
        return result


def handle_row(row):
    return 0


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    instance = PulseTrain(input)
    sum = instance.solve()

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Difference, expected={expected}, actual={sum}, diff = {sum - expected}")
            if abs(sum) > 99000:
                print(f"{sum} <= actual")
                print(f"{expected} <= expected")

    return sum


res = run("test_20.txt", expected=32000000)
res = run("test_20b.txt", expected=11687500)

print()
res = run("data_20.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
