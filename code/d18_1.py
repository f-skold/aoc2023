from typing import List

import common
import common_grid_coords
from common_grid_coords import Coord, Direction

MAPPING = {
    "U": Direction.NORTH,
    "D": Direction.SOUTH,
    "L": Direction.WEST,
    "R": Direction.EAST,
}


class LavaPool:
    def __init__(self, input):
        # self.map
        self.instructions = []
        for row in input:
            temp = row.strip().split(" ")
            temp[1] = int(temp[1])
            self.instructions.append(temp)
        self.map = []
        self.max_coord = Coord(0, 0)
        self.start = None
        self.flood_fill_queue = []
        self.visited = set()

    def flood_fill(self, x, y):
        if (x, y) not in self.visited:
            self.flood_fill_inner(x, y)
            item = (x, y)
            self.visited.add(item)

        while len(self.flood_fill_queue):
            item = self.flood_fill_queue.pop()
            if item not in self.visited:
                self.flood_fill_inner(item[0], item[1])
                self.visited.add(item)

    def flood_fill_inner(self, x, y):
        if x < 0 or y < 0 or x >= self.max_coord.x or y >= self.max_coord.y:
            return

        square = self.map[y][x]
        if "." != square:
            return
        self.map[y][x] = "Y"
        self.flood_fill_queue.append((x + 1, y))
        self.flood_fill_queue.append((x - 1, y))
        self.flood_fill_queue.append((x, y - 1))
        self.flood_fill_queue.append((x, y + 1))

    def draw(self):
        origin = Coord(0, 0)
        coord = origin
        max_coord = origin
        min_coord = origin
        for index, inst in enumerate(self.instructions):
            vector1 = common_grid_coords.MOVEMENT[MAPPING[inst[0]]]
            vector1 = common_grid_coords.mult_scalar(inst[1], vector1)
            next = common_grid_coords.add(coord, vector1)
            max_coord = common_grid_coords.coord_max(max_coord, next)
            min_coord = common_grid_coords.coord_min(min_coord, next)
            coord = next
            # self.map[next.y][next.x] = "#"
            # print(f"{index}: {coord}")

        print(f"max: {max_coord}, min: {min_coord}")

        start = common_grid_coords.coord_min(origin, min_coord)
        self.max_coord = common_grid_coords.sub(max_coord, start)
        # max_coord = self.max_coord
        self.start = common_grid_coords.sub(origin, start)
        print(f"new_max: {self.max_coord}, start: {self.start}")
        for _ in range(self.max_coord.y + 1):
            self.map.append(["." for _ in range(self.max_coord.x + 1)])
        coord = self.start
        self.map[coord.y][coord.x] = "S"
        for index, inst in enumerate(self.instructions):
            vector1 = common_grid_coords.MOVEMENT[MAPPING[inst[0]]]
            for _ in range(inst[1]):
                next = common_grid_coords.add(coord, vector1)
                try:
                    self.map[next.y][next.x] = "#"
                except Exception as e:
                    print(f"ERROR: index={index}, {next}")
                    raise e
                coord = next
        coord = self.start
        self.map[coord.y][coord.x] = "S"
        return

    def solve(self, game_b=False) -> int:
        self.draw()
        walls1 = 0
        walls2 = 0
        coord = self.start
        self.map[coord.y][coord.x] = "#"
        for row in self.map:
            walls2 += self.max_coord.x + 1 - row.count(".")
            walls1 += row.count("#")

        # common.matrix_print(self.map)
        print()
        self.flood_fill(self.start.x + 1, self.start.y)
        area = 0
        for row in self.map:
            area += self.max_coord.x + 1 - row.count(".")
        # common.matrix_print(self.map)
        print(f"Walls={walls1}, {walls2} area={area}")
        return area


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum = 0
    instance = LavaPool(input)
    sum = instance.solve()

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


res = run("test_18.txt", expected=62)
print()
res = run("data_18.txt")

to_high: List[int] = []
to_low: List[int] = [
    48570,  # 2
    4099,  # 1
]
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
