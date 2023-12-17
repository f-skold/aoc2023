import copy
import pprint
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

NUM_MAPPING = [
    Direction.EAST,  # R
    Direction.SOUTH,  # D
    Direction.WEST,  # L
    Direction.NORTH,  # U
]


class LavaPool:
    def __init__(self, input):
        # self.map
        self.instructions = []
        for index, row in enumerate(input):
            row = row.strip()
            temp = row.split(" ")
            # temp[1] = int(temp[1])
            hex = temp[2][2:7]
            num_dir = int(temp[2][7])
            item = (NUM_MAPPING[num_dir], int(f"0x{hex}", 16))
            # print(f"{index} : {temp[2]}, {item},  {row}")
            self.instructions.append(item)
        self.map = []
        self.max_coord = Coord(0, 0)
        self.start = None
        self.flood_fill_queue = []
        self.visited = set()
        self.ranges = []

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

    def add_ranges(self, meta: int, y_range, x_range):
        if 0 == len(self.ranges):
            self.ranges = [[y_range] + x_range]
            if False:
                print("initial")
                pprint.pprint(self.ranges)

            return
        pos = 0
        y_min = y_range[0]
        y_max = y_range[1]
        # print(f"ADD: meta={meta}, y_range={y_range}, x_range={x_range}")

        # prev_range = None
        out = copy.deepcopy(self.ranges)
        for index, value in enumerate(self.ranges):
            print(f"ix={index}, v={value}")
            curr = value[0]
            if curr[1] < y_min:
                # prev_range = curr
                continue
            # overlap
            # Knows:  y_min <= curr[1]

            new_ranges = []
            y = min(curr[0], y_min)
            if curr[0] < y_min:
                # old starts before
                print("case 1A")
                new_ranges += [(curr[0], y_min - 1), value[1:]]

            array = list(sorted(value[1:] + x_range))
            y = min(y_max, curr[1])
            new_ranges.append([(y_min, y)] + array)
            if y < curr[1]:
                print("case 2A")
                new_ranges.append([(y + 1, curr[1])] + value[1:])
            elif y < y_max:
                print("case 2B")
                new_ranges.append([(y + 1, y_max)] + x_range)
            print(f"After xxx, index={index}, {new_ranges}")
            # self.ranges[index:index+1] = new_ranges

            out[index] = new_ranges[0]
            pos = index + 1
            for xxx in new_ranges[1:]:
                out.insert(index, pos)
                pos += 1

        self.ranges = out
        # pprint.pprint(self.ranges)
        # overlaps:
        # 000  11111     22222
        #     aaaaaaaaa     bb
        #
        #      111111  22222 3333444
        #      aaaa  bbbbbb cc  dd

    def draw(self):
        origin = Coord(0, 0)
        the_start = Coord(0, 0)
        coord = the_start
        max_coord = coord
        min_coord = coord
        coords = [coord]
        for index, inst in enumerate(self.instructions):
            dir = inst[0]
            vector1 = common_grid_coords.MOVEMENT[dir]
            vector2 = common_grid_coords.mult_scalar(inst[1], vector1)
            next = common_grid_coords.add(coord, vector2)
            max_coord = common_grid_coords.coord_max(max_coord, next)
            min_coord = common_grid_coords.coord_min(min_coord, next)
            # y_range = sorted([coord.y, next.y])
            # x_range = list(sorted([coord.x, next.x]))

            coord = next
            coords.append(next)
            # self.map[next.y][next.x] = "#"
            # print(f"{index}: {coord}")

        # coords.append(origin)
        print(f"max: {max_coord}, min: {min_coord}")
        self.coords = coords

        start = common_grid_coords.coord_min(origin, min_coord)
        self.max_coord = common_grid_coords.sub(max_coord, start)

        temp1 = set(map(lambda c: c.y - start.y, coords))
        temp2 = set(map(lambda c: c.x - start.x, coords))
        y_coords = list(sorted(temp1))
        x_coords = list(sorted(temp2))
        # print("x_coords", x_coords)
        # print("y_coords", y_coords)

        self.big_map = []
        for _ in range(len(y_coords) * 3):
            self.big_map.append(["." for _ in range(len(x_coords) * 3)])

        self.y_coords = y_coords
        self.ranges = {}
        for y in y_coords:
            self.ranges[y] = []

        # max_coord = self.max_coord
        self.start = common_grid_coords.sub(origin, start)
        # self.start = the_start
        print(f"new_max: {self.max_coord}, start: {self.start}")
        coords = [self.start]
        coord = self.start
        prev_pos = 0
        # self.ranges[coord.y].append(coord.x)
        self.borders = 0
        for index, inst in enumerate(self.instructions):
            try:
                prev = coord
                # prev_char = Coord(x_coords.index(prev.x) * 3, y_coords.index(prev.y) * 3)
                dir = inst[0]
                length = inst[1]
                vector1 = common_grid_coords.MOVEMENT[dir]
                vector2 = common_grid_coords.mult_scalar(length, vector1)
                self.borders += length
                coord = common_grid_coords.add(coord, vector2)
                # coord_char = Coord(x_coords.index(coord.x) * 3, y_coords.index(coord.y) * 3)
                # char = prev_char
                # while char != coord_char:
                #    self.big_map[char.y][char.x] = "#"
                #    char = common_grid_coords.add(char, vector1)

                coords.append(coord)
                pos = y_coords.index(coord.y)
            except Exception as e:
                print(f"index={index}: prev={prev}, coord={coord}")
                raise e

            if dir in [Direction.EAST, Direction.WEST]:
                self.ranges[coord.y].append(prev.x)
                self.ranges[coord.y].append(coord.x)
            else:
                temp = sorted([prev_pos, pos])
                for ix in range(temp[0], temp[1] + 1):
                    self.ranges[y_coords[ix]].append(coord.x)
            prev_pos = pos

        self.coords = coords
        return

    def calc_from_area_formula(self):
        sum = 0
        print(self.coords[-1])
        curr = self.coords[0]
        for index in range(len(self.coords) - 1):
            next = self.coords[index + 1]
            sum += curr.x * next.y - next.x * curr.y
            curr = next
        return sum // 2 + (self.borders // 2 + 1)

    def solve(self, game_b=False) -> int:
        self.draw()
        walls1 = 0
        walls2 = 0

        common.matrix_print(self.big_map)

        sum = 0
        for y in self.y_coords:
            list(sorted(set(self.ranges[y])))
            # print(f"R: {y}, {line}")

        print(self.coords[-1])
        curr = self.coords[0]
        for index in range(len(self.coords) - 1):
            next = self.coords[index + 1]
            sum += curr.x * next.y - next.x * curr.y
            curr = next
        return sum // 2 + (self.borders // 2 + 1)

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
            print(f"Difference, expected={expected}, actual={sum}, diff = {sum - expected}")
            print(f"{sum} <= actual")
            print(f"{expected} <= expected")
    return sum


res = run("test_18.txt", expected=952408144115)
print()
res = run("data_18.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
