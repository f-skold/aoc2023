import common
import common_grid_coords
from common_grid_coords import Coord, Direction

# - | \ /
# N=0, E=1, S=2, W=3

# /
MIRROR_FORWARD = {
    Direction.NORTH: Direction.EAST,
    Direction.EAST: Direction.NORTH,
    Direction.SOUTH: Direction.WEST,
    Direction.WEST: Direction.SOUTH,
}

# \
MIRROR_BACKSLASH = {
    Direction.NORTH: Direction.WEST,
    Direction.WEST: Direction.NORTH,
    Direction.SOUTH: Direction.EAST,
    Direction.EAST: Direction.SOUTH,
}


class Reflectors:
    def __init__(self, input):
        self.map = []
        self.energized = []
        self.beams = []
        for row in input:
            self.map.append([c for c in row.strip()])

        self.y_size = len(self.map)
        self.x_size = len(self.map[0])
        self.queue = []
        self.memory = {}
        self.energized = []
        self.beams = []
        self.reset()

    def reset(self):
        self.queue = []
        self.memory = {}

        self.energized = []
        self.beams = []
        for row in self.map:
            self.energized.append([0 for _ in range(self.x_size)])
            self.beams.append([0 for _ in range(self.x_size)])

    def flow(self, dir: Direction, coord: Coord):
        self.queue.append((dir, coord))

    def valid(self, coord: Coord) -> bool:
        return 0 <= coord.x and coord.x < self.x_size and 0 <= coord.y and coord.y < self.y_size

    def run_flow(self, dir: Direction, coord: Coord):
        if not self.valid(coord):
            return
        char = self.map[coord.y][coord.x]
        self.energized[coord.y][coord.x] += 1
        dir2value = 2**dir.value
        if dir2value & self.beams[coord.y][coord.x]:
            return
        self.beams[coord.y][coord.x] |= dir2value
        move = common_grid_coords.MOVEMENT
        match char:
            case ".":
                new_coord = common_grid_coords.add(coord, move[dir])
                self.flow(dir, new_coord)
            case "|":
                if dir in [Direction.EAST, Direction.WEST]:
                    self.flow(Direction.NORTH, coord)
                    self.flow(Direction.SOUTH, coord)
                else:
                    new_coord = common_grid_coords.add(coord, move[dir])
                    self.flow(dir, new_coord)

            case "-":
                if dir in [Direction.NORTH, Direction.SOUTH]:
                    self.flow(Direction.EAST, coord)
                    self.flow(Direction.WEST, coord)
                else:
                    new_coord = common_grid_coords.add(coord, move[dir])
                    self.flow(dir, new_coord)
            case "/" | "\\":
                if "/" == char:
                    new_dir = MIRROR_FORWARD[dir]
                else:
                    new_dir = MIRROR_BACKSLASH[dir]
                new_coord = common_grid_coords.add(coord, move[new_dir])
                self.flow(new_dir, new_coord)

    def solve_once(self, dir, coord) -> int:
        self.reset()
        self.flow(dir, coord)

        while len(self.queue):
            item = self.queue.pop()
            self.run_flow(item[0], item[1])

        # common.matrix_print(self.energized)
        sum = 0
        for row in self.energized:
            sum += self.x_size - row.count(0)
        return sum

    def solve(self, game_b=False) -> int:
        max = 42
        max_coord = None
        for x in range(self.x_size):
            coord = Coord(x, 0)
            points = self.solve_once(Direction.SOUTH, coord)
            if points > max:
                max = points
                max_coord = coord

            coord = Coord(x, self.y_size - 1)
            points = self.solve_once(Direction.NORTH, coord)
            if points > max:
                max = points
                max_coord = coord

        for y in range(self.y_size):
            coord = Coord(0, y)
            points = self.solve_once(Direction.EAST, coord)
            if points > max:
                max = points
                max_coord = coord

            coord = Coord(0, self.x_size - 1)
            points = self.solve_once(Direction.WEST, coord)
            if points > max:
                max = points
                max_coord = coord
        print(f"max is {max} for {max_coord}")
        return max


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    sum = 0
    if True:
        reflectors = Reflectors(input)
        sum = reflectors.solve()

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


res = run("test_16.txt", expected=46)
print()
res = run("data_16.txt")
