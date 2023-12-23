from typing import List

import common
import common_grid_coords
from common_grid_coords import Coord2

INFINITY = 111999222000


FORCED_MOVEMENT = {
    "^": Coord2(0, -1),
    "v": Coord2(0, 1),
    ">": Coord2(1, 0),
    "<": Coord2(-1, 0),
}


class LongestPath:
    def __init__(self, input):
        self.maze = []
        self.distance = []
        for row in input:
            maze_row = [c for c in row.strip()]
            self.maze.append(maze_row)
            self.distance.append([0 for _ in maze_row])
        self.y_size = len(self.maze)
        self.x_size = len(self.maze[0])
        self.start = Coord2(self.maze[0].index("."), 0)
        self.end = Coord2(self.maze[-1].index("."), self.y_size - 1)

        self.neighbour_vectors = common_grid_coords.MOVEMENT.values()
        self.infinity = (1 + self.x_size) * (1 + self.y_size)
        self.queue = []

    def try1(self, pos: Coord2, path_len, visited):
        # print(f"try1: {pos}, {path_len}")
        prev_dist = self.distance[pos.y][pos.x]
        if pos in visited:
            return

        if path_len < prev_dist:
            return
        self.distance[pos.y][pos.x] = path_len
        char = self.maze[pos.y][pos.x]
        candidates = []
        if char in FORCED_MOVEMENT:
            next = common_grid_coords.add2(pos, FORCED_MOVEMENT[char])
            candidates = [next]
        elif "." == char:
            for vect in self.neighbour_vectors:
                next = common_grid_coords.add2(pos, vect)
                if pos in visited:
                    continue
                if 0 <= next.y and next.y < self.y_size:
                    next_char = self.maze[next.y][next.x]
                    if "#" != next_char:
                        candidates.append(next)
        else:
            raise Exception(f"Stange char {char} at {pos}")

        new_len = path_len + 1
        new_visited = visited.copy() + [pos]
        for cand in candidates:
            item = (cand, new_len, new_visited)
            self.queue.append(item)
            # self.try1(cand, new_len, new_visited)

    def solve(self, game_b=False) -> int:
        self.queue = [(self.start, 0, [])]
        while len(self.queue):
            pos, traveled, visited = self.queue.pop()
            self.try1(pos, traveled, visited)

        # common.matrix_print(self.distance)
        common.matrix_print(self.maze)
        return self.distance[self.end.y][self.end.x]


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum1 = 0
    instance = LongestPath(input)
    sum1 = instance.solve()

    print(f"Sum is {sum1}")
    if expected is not None:
        if expected == sum1:
            print("** Correct")
        else:
            print(f"Difference, expected={expected}, actual={sum1}, diff = {sum1 - expected}")
            if abs(sum1) > 99000:
                print(f"{sum1} <= actual")
                print(f"{expected} <= expected")

    return sum1


res = run("test_23.txt", expected=94)
print()
res = run("data_23.txt")

to_high: List[int] = []
to_low: List[int] = []
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
