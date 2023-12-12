from enum import IntEnum

import common

CONNECTS = {
    0: 2,
    1: 3,
    2: 0,
    3: 1,
}

MOVEMEMT = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0),
}
PIPES = {
    "|": (0, 2),
    "-": (1, 3),
    "L": (0, 1),
    "J": (0, 3),
    "7": (2, 3),
    "F": (1, 2),
}

CORNERS = {
    "F": [(1, 1)],
    "L": [(1, -1)],
    "7": [(-1, 1)],
    "J": [(-1, -1)],
}

EMPTY_SQUARES = [".", "I", "O"]


class NeigbourSquare(IntEnum):
    EMPTY = 0
    OTHER_WALL = 1
    MY_WALL = 2
    TEMP_FILLED = 3
    INSIDE_FILLED = 4


def add(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1])


class BadAreaException(Exception):
    pass

    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # . is ground; there is no pipe in this tile.
    # S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.


class Maze:
    def __init__(self, input):
        self.grid = list(input)
        self.y_size = len(input)
        self.x_size = len(input[0].strip())
        for y, row in enumerate(input):
            self.grid[y] = row.strip()
            for x, char in enumerate(row):
                if "S" == char:
                    self.start = (x, y)
                    continue
        self.visited = []
        self.neighbours = []
        for y in range(self.y_size):
            self.visited.append([0 for x in range(self.x_size)])
            self.neighbours.append([NeigbourSquare.EMPTY for x in range(self.x_size)])
        sx, sy = self.start
        print(f"Start: x={sx}, y={sy}")
        to_try = [(sx, sy - 1, 0), (sx + 1, sy, 1), (sx, sy + 1, 2), (sx - 1, sy, 3)]
        accepted = []
        for index, square in enumerate(to_try):
            tx, ty, dir = square
            if tx < 0 or ty < 0:
                continue
            char = self.grid[ty][tx]
            if "." == char:
                continue
            connections = PIPES[char]
            new_dir = (dir + 2) % 4
            print(f"{square}, {dir} -> {new_dir} in {connections} : {char}")
            if new_dir in connections:
                accepted.append(square)

        self.accepted = accepted
        dirs = (accepted[0][2], accepted[1][2])
        for k, v in PIPES.items():
            if dirs == v:
                temp = list(self.grid[sy])
                temp[sx] = k
                self.grid[sy] = "".join(temp)
        print(f"accepted = {accepted}, {self.grid[sy][sx]}")

    def walk_maze(self):
        # start square
        count = 0
        x, y = self.start
        self.visited[y][x] = count + 1
        self.neighbours[y][x] = NeigbourSquare.MY_WALL
        dir = self.accepted[0][2]
        old_dir = dir
        next = MOVEMEMT[dir]
        x += next[0]
        y += next[1]

        visited_squares = [self.start]
        while (x, y) != self.start:
            visited_squares.append((x, y))
            new_dir = (old_dir + 2) % 4
            count += 1
            char = self.grid[y][x]
            self.visited[y][x] = count
            self.neighbours[y][x] = NeigbourSquare.MY_WALL
            connections = PIPES[char]
            if new_dir == connections[0]:
                dir = connections[1]
            elif new_dir == connections[1]:
                dir = connections[0]
            else:
                raise Exception(f"At position (x={x}, y={y}), old_dir={old_dir} {new_dir} not in {connections}")
            old_dir = dir
            next = MOVEMEMT[dir]
            x += next[0]
            y += next[1]
            # print(f"{count}: {x}, {y} : {char} => {connections}. {old_dir} > {dir}")
        self.visited[y][x] = count
        self.neighbours[y][x] = NeigbourSquare.MY_WALL
        self.visited_squares = visited_squares
        return (count + 1) // 2

    def _flood_fill(self, x, y, dir):
        if x < 0 or y < 0 or x >= self.x_size or y >= self.y_size:
            return
        neighbours = self.neighbours[y][x]
        if NeigbourSquare.TEMP_FILLED == neighbours:
            return
        elif NeigbourSquare.EMPTY != neighbours:
            self._walls.append((x, y))
            return
        char = self.grid[y][x]
        if char in EMPTY_SQUARES:
            self.neighbours[y][x] = NeigbourSquare.TEMP_FILLED
            self._area.append((x, y))
            self._flood_fill(x + 1, y, 1)
            self._flood_fill(x - 1, y, 3)
            self._flood_fill(x, y - 1, 0)
            self._flood_fill(x, y + 1, 2)
        elif self.visited[y][x] or (NeigbourSquare.MY_WALL == self.neighbours[y][x]):
            # self.neighbours[y][x] = MY_WALL
            self._walls.append((x, y))
            return
        else:
            self.neighbours[y][x] = NeigbourSquare.OTHER_WALL
            self._walls.append((x, y))
            # raise BadAreaException(f"Other wall at {x}, {y}")

    def one_area(self, try_coord):
        # print(f"One area - entering: {try_coord}")
        self._area = []
        self._walls = []
        try:
            tx, ty = try_coord
            dir = -1
            self._flood_fill(tx, ty, dir)
        except BadAreaException as e:
            self._area = []
            self._walls = []
            print(e)

        if len(self._area):
            walls = set(self._walls)
            other_walls = walls.difference(self.set_of_visited_squares)
            if len(other_walls):
                print(f"One area, other walls: {try_coord}, area={len(self._area)}, {other_walls}")
                return 0
            for square in self._area:
                x, y = square
                self.neighbours[y][x] = NeigbourSquare.INSIDE_FILLED
            # non empty
            # nop = walls.intersection(self.set_of_visited_squares)
            print(f"One area: {try_coord}, area={len(self._area)}")
        return len(self._area)

    def find_inside(self):
        for y, row in enumerate(self.grid):
            prev_x = NeigbourSquare.OTHER_WALL
            for x, char in enumerate(row.strip()):
                if char in EMPTY_SQUARES:
                    pass
                else:
                    if NeigbourSquare.MY_WALL != self.neighbours[y][x]:
                        self.neighbours[y][x] = NeigbourSquare.OTHER_WALL
                        # print(f"find_inside early: OTHER_WALL {x}, {y}, {char}")
        self.set_of_visited_squares = set(self.visited_squares)

        # y_count_l = [0 for x in range(self.x_size)]
        # y_count_r = [0 for x in range(self.x_size)]
        count_u = 0
        count_l = 0
        sum = 0
        for y in range(self.y_size):
            prev_x = NeigbourSquare.OTHER_WALL
            for x in range(self.x_size):
                square = self.neighbours[y][x]
                if NeigbourSquare.MY_WALL == square:
                    grid_char = self.grid[y][x]
                    if grid_char in ["|", "L", "J"]:
                        count_u += 1
                    if grid_char in ["|", "F", "7"]:
                        count_l += 1

                    # if grid_char in ["-", "J", "7"]:
                    #     y_count_l[x] += 1
                    # if grid_char in ["-", "L", "F"]:
                    #     y_count_r[x] += 1
                elif NeigbourSquare.EMPTY == square and (count_u % 2) and (count_l % 2):
                    # and (y_count_l[x] % 2) and (y_count_r[x] % 2):
                    if NeigbourSquare.MY_WALL == prev_x or NeigbourSquare.MY_WALL == self.neighbours[y - 1][x]:
                        coord = (x, y)
                        sum += self.one_area(coord)
                prev_x = self.neighbours[y][x]

        return sum

    def plot(self):
        for y, row in enumerate(self.neighbours):
            s = ""
            for x, square in enumerate(row):
                c = " "
                match square:
                    case NeigbourSquare.MY_WALL:
                        # c = "X"
                        c = self.grid[y][x]
                    case NeigbourSquare.INSIDE_FILLED:
                        c = "#"
                    case NeigbourSquare.TEMP_FILLED:
                        c = "/"
                    case NeigbourSquare.OTHER_WALL:
                        c = "."
                    case NeigbourSquare.EMPTY:
                        c = "e"

                s += c
            s += f" : {y}"
            print(s)
        s0 = ""
        s1 = ""
        for x in range(self.x_size):
            s0 += f"{x % 10}"
            s1 += f"{(x // 10) % 10}"
        print()
        print(s1)
        print(s0)


def run(filename, ans=None):
    print()
    input = common.read_file_contents(filename)
    maze = Maze(input)
    maze.walk_maze()
    ans1 = maze.find_inside()
    maze.plot()
    print(f"Area is {ans1}")
    if ans is not None and ans != ans1:
        print(f"DIFFER: Expected {ans}, got {ans1}")
    return ans1


res = run("test_10b1.txt", ans=4)
res = run("test_10b2.txt", ans=4)
res = run("test_10b3.txt", ans=8)
print()
res = run("data_10.txt")
# 42, 16, 12, 24, 467
