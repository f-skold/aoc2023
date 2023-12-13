from typing import List

import common


def compare(row1, row2, max_differences=1) -> int:
    len1 = len(row1)
    assert len1 == len(row2)
    differences = 0
    for i in range(len1):
        if row1[i] != row2[i]:
            differences += 1
            if differences > max_differences:
                break
    return differences


class LabyrithMirrors:
    def __init__(self, input, debug=True):
        self.grids = []
        self.sum = 0
        self._debug = debug

        current = []
        for row in input:
            temp = row.strip()
            if 0 != len(temp):
                current.append(temp)
            else:
                self.grids.append(current)
                current = []
        if len(current):
            self.grids.append(current)

    def process_one(self, index, grid, mult=1) -> int:
        row_count = len(grid)
        for y, row in enumerate(grid):
            self.y = y
            to_check = min(y + 1, row_count - y - 1)
            diffs = 0
            if to_check >= 1:
                diffs = compare(row, grid[y + 1])
                if diffs < 2:
                    if self._debug:
                        print(f"{index} : y={y}, row_count={row_count}, to_check={to_check}")
                    offset = 1
                    while diffs < 2 and offset < to_check:
                        self.offset = offset
                        if self._debug:
                            print(f"{index} : Checking y={y}, offset={offset},  {y - offset}, {y + 1 + offset}")
                        diffs += compare(grid[y - offset], grid[y + 1 + offset], max_differences=(1 - diffs))
                        offset += 1

                    if diffs == 1:
                        if self._debug:
                            print(f"{index} : returning for {y}")
                        return mult * (y + 1)
                    elif diffs == 0:
                        if self._debug:
                            print(f"{index} : {y} had no smudged mirror")

        return 0

    def transpose(self, grid):
        t = []
        x_size = len(grid[0])
        y_size = len(grid)
        for x in range(x_size):
            column = [grid[y][x] for y in range(y_size)]
            t.append(column)
        return t

    def _print(self, grid):
        for i, row in enumerate(grid):
            value = 0
            pow = 1
            string = ""
            for c in row:
                string += c
                if "#" == c:
                    value += pow
                pow *= 2
            print(f"{string} : {i}, {value:06x}")

    def solve(self) -> int:
        sum = 0
        for i, grid in enumerate(self.grids):
            try:
                from_cols = 0
                from_rows = 0
                if False:
                    print(f"Index {i}, transposed")
                    transposed = self.transpose(grid)
                    if self._debug:
                        self._print(transposed)
                    from_cols = self.process_one(i + 100, transposed, mult=1)
                    sum += from_cols

                if 0 == from_cols:
                    print(f"Index {i}")
                    if self._debug:
                        self._print(grid)

                    from_rows = self.process_one(i, grid, mult=100)
                    if from_rows > 0:
                        print(f"from_rows={from_rows}")
                        sum += from_rows

                if 0 == from_rows:
                    print()
                    print(f"Index {i}, transposed")
                    transposed = self.transpose(grid)
                    if self._debug:
                        self._print(transposed)
                    from_cols = self.process_one(i + 100, transposed, mult=1)
                    sum += from_cols

                if 0 == from_cols and 0 == from_rows:
                    raise ValueError(f"No value, index {i}")
                    print(f"NOTE: from_cols={from_cols}")
                    sum += from_cols
            except Exception as e:
                print(f"index={i} : y={self.y}, offset={self.offset}")
                raise e
        return sum

    # 0 #.##..##.
    # 1 ..#.##.#.
    # 2 ##......#
    # 3 ##......#
    # 4 ..#.##.#.
    # 5 ..##..##.
    # 6 #.#.##.#.


def run(filename, game_b=False, expected=None):
    input = common.read_file_contents(filename)
    labyrith = LabyrithMirrors(input)
    sum = labyrith.solve()
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        assert expected == sum, f"Difference, expected={expected}, actual={sum}"
        print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


# res = run("test_13.txt", expected=405)
res = run("test_13.txt", game_b=True, expected=400)
res = run("test_13b.txt", game_b=True, expected=8)
print()
res = None
res = run("data_13.txt")
to_low: List[int] = []
to_high: List[int] = [
    42282,  # 1
]
if res is not None:
    manpen = 31108
    if res != manpen:
        print(f"Manpen had {manpen} != {res}, diff={res - manpen}")
    if len(to_low) and res <= to_low[0]:
        print(f"Result {res} is to low.")
    elif len(to_high) and res >= to_high[0]:
        print(f"Result {res} is to high.")
