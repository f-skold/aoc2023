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
            for x, char in enumerate(row):
                if "S" == char:
                    self.start = (x, y)
                    continue
        self.visited = []
        for y in range(self.y_size):
            self.visited.append([0 for x in range(self.x_size)])
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
        print(f"accepted = {accepted}")
        self.accepted = accepted

    def walk_maze(self):
        # start square
        count = 0
        x, y = self.start
        self.visited[y][x] = count
        dir = self.accepted[0][2]
        old_dir = dir
        next = MOVEMEMT[dir]
        x += next[0]
        y += next[1]

        while (x, y) != self.start:
            new_dir = (old_dir + 2) % 4
            count += 1
            char = self.grid[y][x]
            self.visited[y][x] = count
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

        return (count + 1) // 2


def run(filename, ans=None):
    input = common.read_file_contents(filename)
    maze = Maze(input)
    ans = maze.walk_maze()
    print(f"Length is {ans}")


expected_tests = 2
res = run("test_10.txt", ans=expected_tests)
print()
res = run("data_10.txt")
