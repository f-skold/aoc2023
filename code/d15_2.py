import collections

import common


def hash(chunk) -> int:
    value = 0
    for char in chunk:
        ascii = ord(char)
        value += ascii
        value = (value * 17) % 256
    return value


class HashMap:
    def __init__(self, input):
        self.chunks = input[0].strip().split(",")
        self.map = collections.defaultdict(list)

    def _dump_box(self, box_num, contents, chunk):
        print(f"{chunk:5} # Box {box_num}: {contents}")

    def solve(self, game_b=False) -> int:
        for chunk in self.chunks:
            temp = chunk.split("=")
            if 2 == len(temp):
                label = temp[0]
                focal = int(temp[1])
                box = hash(label)
                lenses = self.map[box]
                found = False
                for index, tuple in enumerate(lenses):
                    lens_label, lens_focal = tuple
                    if label == lens_label:
                        found = True
                        lenses[index] = (label, focal)
                if not found:
                    lenses.append((label, focal))
                # self._dump_box(box, lenses, chunk)

            elif chunk.endswith("-"):
                label = chunk[:-1]
                box = hash(label)
                lenses = self.map[box]
                for lens_label, lens_focal in lenses:
                    if label == lens_label:
                        lenses.remove((label, lens_focal))
                        break
                # self._dump_box(box, lenses, chunk)
            else:
                raise Exception(f"Unhandled chunk {chunk}")

        sum = 0
        for box, lenses in self.map.items():
            for index, tuple in enumerate(lenses):
                local = (1 + box) * (1 + index) * tuple[1]
                # print(f"{tuple[0]} :  {1 + box} * {1 + index} * {tuple[1]} : {local}")
                sum += local
        return sum


def handle_row(row) -> int:
    chunks = row.split(",")
    value = 0
    for chunk in chunks:
        temp = hash(chunk)
        print(f"{temp:4} : {chunk}")
        value += temp
    return value


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    sum = 0
    # for row in input:
    #     sum += handle_row(row.strip())

    instance = HashMap(input)
    sum = instance.solve()
    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


# rn=1 becomes 30.
# cm- becomes 253.
# qp=3 becomes 97.
# cm=2 becomes 47.
# qp- becomes 14.
# pc=4 becomes 180.
# ot=9 becomes 9.
# ab=5 becomes 197.
# pc- becomes 48.
# pc=6 becomes 214.
# ot=7 becomes 231.


res = run("test_15.txt", expected=145)
print()
res = run("data_15.txt")
