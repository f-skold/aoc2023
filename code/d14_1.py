import copy

import common


class Tilt:
    def __init__(self, input):
        grid = []
        for row in input:
            grid.append([c for c in row.strip()])
        self.transposed_grid = common.transpose(grid)

    def solve(self, game_b=False) -> int:
        score = 0
        x_size = len(self.transposed_grid[0])
        # common.matrix_print(self.transposed_grid)
        grid2 = []
        for i, row in enumerate(self.transposed_grid):
            local_score = 0
            pos = 0
            old_row = copy.copy(row)
            while pos >= 0 and pos < x_size:
                try:
                    needle = row.index(".", pos)
                    # print(f"row {i}, found empty {needle}")
                except ValueError:
                    pos = -1
                    break
                empty_space = needle
                # search for next O, #
                pos = -1
                for index in range(empty_space + 1, x_size):
                    if "#" == row[index]:
                        pos = index + 1
                        break
                    elif "O" == row[index]:
                        row[empty_space] = row[index]
                        row[index] = "."
                        pos = empty_space + 1
                        break
            for i, c in enumerate(row):
                if "O" == c:
                    local_score += x_size - i
            if False:
                print(f"{''.join(old_row)} : {i} original")
                print(f"{''.join(row)} : {i} modified, local_score={local_score}")
                print()

            grid2.append(row)
            score += local_score

        print()
        # common.matrix_print(grid2)
        return score


def run(filename, expected=None):
    input = common.read_file_contents(filename)
    tilt = Tilt(input)

    sum = tilt.solve()
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")


res = run("test_14.txt", expected=136)
print()
# 110779
res = run("data_14.txt")
