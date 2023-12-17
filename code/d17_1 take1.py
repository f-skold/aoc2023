import queue
import collections

import common
import common_grid_coords
from common_grid_coords import Coord, Direction

INFINITY = 10009992225555000111


def constant_factory(value):
    return lambda: value


class TraverseMap:
    def __init__(self, input):
        self.map = []
        for row in input:
            self.map.append([int(c) for c in row.strip()])
        self.y_size = len(self.map)
        self.x_size = len(self.map[0])
        # self.dir = Direction.WEST

        self.open_set2 = []
        self.open_set = queue.PriorityQueue()
        self.came_from = {}
        self.g_score = collections.defaultdict(constant_factory(INFINITY))
        self.f_score = collections.defaultdict(constant_factory(INFINITY))

    def solve(self, game_b=False) -> int:
        # Try both W, S?
        start = Coord(0, 0)
        end = Coord(self.x_size - 1, self.y_size - 1)
        print(start, end)
        return self.a_star(start, end)

    def _get_next_directions(self, current):
        current_coord = current[0]
        current_dir = current[2]
        output = []
        if current_dir in [Direction.NORTH, Direction.SOUTH]:
            if current_coord.x > 0:
                output.append(Direction.WEST)
            if current_coord.x < self.x_size - 1:
                output.append(Direction.EAST)
        elif current_dir in [Direction.EAST, Direction.WEST]:
            if current_coord.y > 0:
                output.append(Direction.NORTH)
            if current_coord.y < self.y_size - 1:
                output.append(Direction.SOUTH)
        return output

    def _valid(self, coord: Coord) -> bool:
        return 0 <= coord.x and coord.x < self.x_size and 0 <= coord.y and coord.y < self.y_size

    def distance(self, current, neighbour):
        cost = 0
        dir = neighbour[2]
        vector = common_grid_coords.MOVEMENT[dir]
        pos = current[0]
        dest = neighbour[0]
        #   print(f"distance: dir={dir}, curr={pos}, dest={dest}, v={vector}")
        while pos != dest:
            pos = common_grid_coords.add(pos, vector)
            cost += self.map[pos.y][pos.x]
        return cost

    # function reconstruct_path(cameFrom, current)
    #     total_path := {current}
    #     while current in cameFrom.Keys:
    #         current := cameFrom[current]
    #         total_path.prepend(current)
    #     return total_path
    def reconstruct_path(self, state):
        total_path = [state[0]]
        current = state
        try:
            while True:
                # current in self.came_from:
                current = self.came_from[current]
                total_path.append(current[0])
        except KeyError:
            pass
        print(list(reversed(total_path)))

    def a_star(self, start_coord: Coord, end: Coord):
        self.end = end
        start1 = (start_coord, 1, Direction.EAST)
        start2 = (start_coord, 2, Direction.SOUTH)
        self.g_score[start1] = 0
        self.g_score[start2] = 0

        self.f_score[start1] = self.heuristics(start1)
        self.f_score[start2] = self.heuristics(start2)
        self.open_set2 = [start1, start2]
        self.open_set.put((self.f_score[start1], start1))
        self.open_set.put((self.f_score[start2], start2))

        while not self.open_set.empty():
            current_item = self.open_set.get()
            current = current_item[1]
            # print(f"Enter item: {current}")
            self.open_set.task_done()
            if current[0] == self.end:
                score = self.g_score[current]
                self.reconstruct_path(current)
                print(f"gScore: {self.g_score[current]}")
                return score
            #
            all_neighbours = []
            current_coord = current[0]
            directions = []
            if current_coord == start_coord:
                directions = [current[2]]
            else:
                directions = self._get_next_directions(current)

            for dir in directions:
                vector = common_grid_coords.MOVEMENT[dir]
                temp = current_coord
                temp = common_grid_coords.add(temp, vector)
                count = 0
                while self._valid(temp) and count < 3:
                    all_neighbours.append((temp, dir.value, dir))
                    temp = common_grid_coords.add(temp, vector)
                    count += 1

            for neighbour in all_neighbours:
                tentative_g_score = self.g_score[current] + self.distance(current, neighbour)
                if tentative_g_score < self.g_score[neighbour]:
                    self.came_from[neighbour] = current
                    self.g_score[neighbour] = tentative_g_score
                    self.f_score[neighbour] = tentative_g_score + self.heuristics(neighbour)

                    if neighbour not in self.open_set2:
                        self.open_set2.append(neighbour)
                        self.open_set.put((self.f_score[neighbour], neighbour))

        return None

    def heuristics(self, current) -> int:
        coord: Coord = current[0]
        guess = common_grid_coords.coord_abs(common_grid_coords.sub(coord, self.end))
        if current[2] in [Direction.NORTH, Direction.WEST]:
            guess += 2
        return guess


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum = 0

    instance = TraverseMap(input)
    sum = instance.solve()

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


res = run("test_17.txt", expected=102)
print()
res = run("data_17.txt")
too_high = [
    1248,  # 1
]
if res >= too_high[0]:
    print(f"Answer {res} is to high, less than {too_high[0]}")
