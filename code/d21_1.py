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
        self.reached = set((self.start,))
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
        for i in range(self.count):
            self.move()
            # print(f"{i+1}: len={len(self.reached)} :  {', '.join(map(str, sorted(self.reached)))}")
            # print()
        return len(self.reached)


def run(filename, count=12, expected=None):
    input = common.read_file_contents(filename)

    instance = RenameMe(input, count)
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


res = run("test_21.txt", count=6, expected=16)
print()
res = run("data_21.txt", count=64)

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
