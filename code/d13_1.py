import common


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
            ok = False
            to_check = min(y + 1, row_count - y - 1)
            if to_check >= 1 and row == grid[y + 1]:
                # print(f"{index} : y={y}, row_count={row_count}, to_check={to_check}")
                ok = True
                for offset in range(1, to_check):
                    self.offset = offset
                    # print(f"{index} : Checking y={y}, offset={offset},  {y - offset}, {y + 1 + offset}")
                    if grid[y - offset] != grid[y + 1 + offset]:
                        ok = False
                        break
                if ok:
                    # print(f"{index} : returning for {y}")
                    return mult * (y + 1)
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
            print(f"{''.join(row)} : {i}")

    def solve(self) -> int:
        sum = 0
        for i, grid in enumerate(self.grids):
            try:
                print(f"Index {i}")
                if self._debug:
                    self._print(grid)
                from_rows = self.process_one(i, grid, mult=100)
                if from_rows > 0:
                    print(f"from_rows={from_rows}")
                    sum += from_rows
                else:
                    transposed = self.transpose(grid)
                    if self._debug:
                        print()
                        self._print(transposed)
                    from_cols = self.process_one(i + 100, transposed, mult=1)
                    if 0 == from_cols:
                        raise ValueError(f"No value, index {i}")
                    print(f"from_cols={from_cols}")
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


def run(filename, expected=None):
    input = common.read_file_contents(filename)
    labyrinth = LabyrithMirrors(input)
    sum = labyrinth.solve()
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


res = run("test_13.txt", expected=405)
print()
res = run("data_13.txt")
to_low = [
    20572,  # 1
]
if res <= to_low[0]:
    print("Result {res} is to low.")
