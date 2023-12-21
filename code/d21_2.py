from typing import List

import common
import common_grid_coords
from common_grid_coords import Coord


class RenameMe:
    def __init__(self, input, count):
        self.count = count
        self.map = []
        self.start = None
        self.time = 0
        self.old_set = set()
        for y, row in enumerate(input):
            array = [c for c in row.strip()]
            self.map.append(array)
            try:
                position = array.index("S")
                self.start = Coord(position, y)
            except Exception:
                pass
        if self.start is None:
            print("Oops, start not set")
        self.max_coord = Coord(len(self.map[0]), len(self.map))
        self.max_coord1 = self.max_coord
        print(f"start1={self.start}, max1={self.max_coord}")
        self.tripple()
        self.tripple()
        self.reached = set((self.start,))

    def tripple(self):
        repeat = 3
        small_map = self.map
        map = []
        for i in range(repeat):
            for row in small_map:
                map.append(row * 3)

        self.start = common_grid_coords.add(self.start, self.max_coord)
        self.map = map
        self.max_coord = Coord(len(self.map[0]), len(self.map))
        print(f"start={self.start}, max={self.max_coord}")

    def check(self, coord: Coord):
        if coord in self.visited:
            return
        self.visited.add(coord)
        if coord.x < 0 or coord.y < 0 or coord.x >= self.max_coord.x or coord.y >= self.max_coord.y:
            return

        if "#" != self.map[coord.y][coord.x]:
            self.reached.add(coord)

    def move(self):
        self.old_set = self.reached
        self.reached = set()
        self.visited = set()
        for coord in self.old_set:
            for delta in common_grid_coords.MOVEMENT.values():
                self.check(common_grid_coords.add(coord, delta))

    def solve(self, game_b=False) -> int:
        self.memory = []
        sample = [65 + (131 * n) for n in range(6)]
        for i in range(self.count):
            self.move()
            # print(f"{i+1}: len={len(self.reached)} :  {', '.join(map(str, sorted(self.reached)))}")
            # print()
            # print(f"{i+1} : {len(self.reached)}")
            if i + 1 in sample:
                # or (60 < i and i < 70) or (120 < i and i < 140) or (186 < i):
                xc = sorted(map(lambda c: c.x, self.reached))
                yc = sorted(map(lambda c: c.y, self.reached))
                xma = xc[-1]
                xmi = xc[0]
                yma = yc[-1]
                ymi = yc[0]
                print(f"  {i+1} :: {len(self.reached)} | {xma-xmi} {xma} {xmi} |  {yma-ymi} {yma} {ymi}")
                self.memory.append((i + 1, len(self.reached)))
            elif i % 5 == 0:
                print(f"  {i+1}")
        return len(self.reached)


def diff_next(level0):
    return [level0[i + 1] - level0[i] for i in range(len(level0) - 1)]


def run(filename, count=12, expected=None):
    input = common.read_file_contents(filename)

    sum = 0
    if False:
        instance = RenameMe(input, 1 + 65 + 4 * 131)
        sum = instance.solve()
        W = instance.max_coord1.x
    else:
        W = 131

    COUNT = 26501365
    mod = COUNT % W
    print("mod", mod)

    t = [mod + (W * n) for n in range(6)]
    t_diff = [t[n] - t[n - 1] for n in range(1, 4)]
    print("t", t)
    print(t_diff)
    # level0 = [3944, 34697, 95903, 190388, 309807]
    level0 = [3944, 35082, 97230, 190388, 314556]
    level1 = diff_next(level0)
    level2 = diff_next(level1)
    # level1 = [level0[1] - level0[0], level0[2] - level0[1]]
    # level2 = level1[1] - level1[0]
    print("level2", level2)
    print("level1", level1)
    print("level0", level0)

    value = level1[0]
    constructed1 = [value]
    for i in range(8):
        value += level2[0]
        constructed1.append(value)
    value = level0[0]
    constructed0 = [value]
    for x in constructed1:
        value += x
        constructed0.append(value)
    print("const0", constructed0)
    print("const1", constructed1)

    a = level2[0] // 2
    b = level1[0] - 3 * a
    c = level0[0] - b - a

    def fn(n):
        return a * n * n + b * n + c

    generated = [fn(n) for n in range(1, 11)]
    print("gen0  ", generated)

    series = (COUNT - 65) // W
    series += 1
    print(series, fn(series))
    sum = fn(series)
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


# res = run("test_21.txt", count=6, expected=16)
print()
res = run("data_21.txt", count=1 + 65 + 2 * 130)

to_high: List[int] = [
    2531010225645512,  # 1
]
to_low: List[int] = [
    632760346904057,  # 3
    632754139050392,  # 2
]
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
