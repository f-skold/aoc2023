import copy

import common

CYCLES = 1000000000
# 1000 000 000


class Tilt:
    def __init__(self, input):
        grid = []
        for row in input:
            grid.append([c for c in row.strip()])
        self.transposed_grid = common.rotate_counter_clockwise(grid)
        self.cycles = 0
        self.print_num = 0
        self.mem = {}

    def matrix_as_string(self):
        out = ""
        for row in self.transposed_grid:
            out += "".join(row) + "|"
        return out

    def matrix_print(self, grid=None, heading=None):
        if grid is None:
            grid = self.transposed_grid
        if heading is None:
            self.print_num += 1
            heading = f"@@ Dumping matrix (count={self.print_num})"
        print(heading)
        common.matrix_print(grid)
        print()

    def calc_score_horiz(self, grid=None) -> int:
        if grid is None:
            grid = common.rotate_counter_clockwise(self.transposed_grid)
        score = 0
        y_size = len(grid)
        for y, row in enumerate(grid):
            score += row.count("O") * (y_size - y)
        return score

    def calc_score(self, grid=None) -> int:
        if grid is None:
            grid = common.rotate_counter_clockwise(self.transposed_grid)
        local_score = 0
        x_size = len(grid[0])
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if "O" == c:
                    local_score += x_size - x
        return local_score

    def solve(self, game_b=False) -> int:
        score = 0
        # self.matrix_print(heading="@ Initial")

        self.one_cycle(initial_rotate=False, dump=False)
        print_grid = common.rotate_two_steps(self.transposed_grid)
        # self.matrix_print(grid=print_grid, heading="@ After 1 cycle:")

        if False:
            for i in range(2, 4):
                self.one_cycle()
                print_grid = common.rotate_two_steps(self.transposed_grid)
                # self.matrix_print(grid=print_grid, heading=f"@ After {i} cycles:")

        no_change = False
        the_cycle = None
        while self.cycles < CYCLES and not (no_change or the_cycle):
            no_change = self.one_cycle()
            key = self.matrix_as_string()
            c = self.cycles
            if key in self.mem:
                the_cycle = c - self.mem[key]
                break
            else:
                self.mem[key] = c
            if 0 == c % 1000:
                print(f"t c={c}")

        if the_cycle:
            print(f"Found a cycle, count={self.cycles}, cycle length={the_cycle}")
            remaining = CYCLES - self.cycles
            loops = remaining // the_cycle
            self.cycles += loops * the_cycle
        print(f"Updated cycle count: {self.cycles}")
        while self.cycles < CYCLES and not no_change:
            no_change = self.one_cycle()
            if 0 == c % 1000:
                print(f"t c={c}")

        print(f"no_change={no_change}, cycles={self.cycles}")
        print_grid = common.rotate_two_steps(self.transposed_grid)
        self.matrix_print(grid=print_grid, heading="@ After many cycles")
        score = self.calc_score_horiz(print_grid)
        print(f"calc_score_horiz: {score}")

        # check_grid = common.rotate_counter_clockwise(self.transposed_grid)
        if False:
            scores = []
            check_grid = common.rotate_clockwise(self.transposed_grid)
            for _ in range(4):
                scores.append(self.calc_score(check_grid))
                check_grid = common.rotate_clockwise(check_grid)
            print(scores)
        return score

    def one_cycle(self, initial_rotate=True, dump=False):
        if initial_rotate:
            self.transposed_grid = common.rotate_clockwise(self.transposed_grid)
        self.start_state = copy.deepcopy(self.transposed_grid)
        self.single_step()
        if dump:
            self.matrix_print()

        self.transposed_grid = common.rotate_clockwise(self.transposed_grid)
        if dump:
            self.matrix_print()
        self.single_step()
        if dump:
            self.matrix_print()

        self.transposed_grid = common.rotate_clockwise(self.transposed_grid)
        self.single_step()

        self.transposed_grid = common.rotate_clockwise(self.transposed_grid)
        self.single_step()

        self.cycles += 1
        return self.transposed_grid == self.start_state

    # before
    # ABCD
    #
    # JKLM

    # after:
    # D  M
    # C  L
    # B  K
    # A  J

    def rotate_counter_clockwise(self):
        new_grid = []
        grid = self.transposed_grid
        y_size = len(grid)
        x_size = len(grid[0])
        for col in range(x_size - 1, -1, -1):
            new_grid.append([grid[y][col] for y in range(y_size)])
        self.transposed_grid = new_grid

    def single_step(self):
        # common.matrix_print(self.transposed_grid)
        x_size = len(self.transposed_grid[0])
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
            if False:
                print(f"{''.join(old_row)} : {i} original")
                print(f"{''.join(row)} : {i} modified, local_score={local_score}")
                print()

            grid2.append(row)
        self.transposed_grid = grid2
        # print()
        # common.matrix_print(grid2)
        return


def run(filename, expected=None):
    input = common.read_file_contents(filename)
    tilt = Tilt(input)

    sum = tilt.solve()
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")


# part 1
# res = run("test_14.txt", expected=136)

res = run("test_14.txt", expected=64)
print()
# part 1, 110779
# part 2, 86069
res = run("data_14.txt")


print(9 + 6 * 3 + (5 + 4) * 2 + 3 * 4 + 2 + 1 * 5)
