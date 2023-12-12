import collections

import common

Coord = collections.namedtuple("Coord", ["x", "y"])

MILLION = 1000000 - 1
# MILLION = 100 - 1


def distance_coord(c1, c2):
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


class Galaxy:
    def __init__(self, input):
        empty_horisontal = []
        y_counts = [0 for _ in range(len(input[0].strip()))]
        for y, row in enumerate(input):
            count = 0
            for x, c in enumerate(row.strip()):
                if "#" == c:
                    count += 1
                    y_counts[x] += 1
            if 0 == count:
                empty_horisontal.append(y)

        x_additions = []
        add = 0
        for x, value in enumerate(y_counts):
            if 0 == value:
                add += MILLION
            x_additions.append(add)

        coords = []
        y_add = 0
        for y, row in enumerate(input):
            if y in empty_horisontal:
                y_add += MILLION
            for x, c in enumerate(row.strip()):
                if "#" == c:
                    coords.append(Coord(x + x_additions[x], y + y_add))
        # print(f"Coords: {coords}")
        self.coords = coords

    def calculate(self):
        sum = 0
        galaxy_count = len(self.coords)
        for i1, c1 in enumerate(self.coords):
            for n2 in range(galaxy_count - i1 - 1):
                i2 = i1 + 1 + n2
                c2 = self.coords[i2]
                diff = distance_coord(c1, c2)

                # print(f"{i1}, {i2} : {diff}  c1={c1}, c2={c2}")
                sum += diff
        return sum

    def plot(self):
        for y, row in enumerate(self.neighbours):
            s = "".join(self.galaxy)
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
    input = common.read_file_contents(filename)
    galaxy = Galaxy(input)
    my = galaxy.calculate()
    print(f"Sum of distances is {my}")
    if ans is not None and ans != my:
        print(f"Diffrence, expected={ans}, actual={my}")


res = run("test_11.txt", ans=374)
print()
res = run("data_11.txt")
