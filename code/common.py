def read_file_contents(filename):
    temp = None
    with open(f"../testdata/{filename}", "rt") as fp:
        temp = fp.readlines()
    return temp


def transpose(grid):
    t = []
    x_size = len(grid[0])
    y_size = len(grid)
    for x in range(x_size):
        column = [grid[y][x] for y in range(y_size)]
        t.append(column)
    return t


def rotate_two_steps(grid):
    new_grid = []
    for row in reversed(grid):
        new_grid.append(list(reversed(row)))
    return new_grid


def rotate_counter_clockwise(grid):
    new_grid = []
    y_size = len(grid)
    x_size = len(grid[0])
    for col in range(x_size - 1, -1, -1):
        new_grid.append([grid[y][col] for y in range(y_size)])
    return new_grid


def rotate_clockwise(grid):
    new_grid = []
    y_size = len(grid)
    x_size = len(grid[0])
    for col in range(x_size):
        new_grid.append([grid[y][col] for y in range(y_size - 1, -1, -1)])
    return new_grid


def matrix_print(grid):
    if isinstance(grid[0], str):
        for i, row in enumerate(grid):
            print(f"{row} : {i}")
    elif isinstance(grid[0], list):
        if isinstance(grid[0][0], str):
            for i, row in enumerate(grid):
                string = "".join(row)
                print(f"{string} : {i}")
        else:
            for i, row in enumerate(grid):
                string = "".join(map(str, row))
                print(f"{string} : {i}")
