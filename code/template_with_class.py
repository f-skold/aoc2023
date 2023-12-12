from typing import List

import common


class RenameMe:
    def __init__(self, input):
        pass

    def solve(self, game_b=False) -> int:
        return 0


def handle_row(row):
    return 0


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum1 = 0
    for row in input:
        sum1 += handle_row(row.strip())

    if True:
        instance = RenameMe(input)
        sum1 = instance.solve()

    print(f"Sum is {sum1}")
    if expected is not None:
        if expected == sum1:
            print("** Correct")
        else:
            print(f"Difference, expected={expected}, actual={sum1}, diff = {sum1 - expected}")
            if abs(sum1) > 99000:
                print(f"{sum1} <= actual")
                print(f"{expected} <= expected")

    return sum1


res = run("test_12.txt", expected=21)
print()
# res = run("data_12.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
