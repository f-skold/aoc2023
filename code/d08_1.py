import common


class Directions:
    def __init__(self, directions):
        self.data = [d for d in directions]
        self.size = len(self.data)
        self.pos = 0
        print(f"Directions: {self.data}")

    def get_choice(self):
        if self.pos >= self.size:
            self.pos -= self.size
        data = self.data[self.pos]
        # print(f"get_choice: {self.pos} {data}")
        self.pos += 1
        return 0 if ("L" == data) else 1


def run(filename, ans=None):
    input = common.read_file_contents(filename)
    directions = input[0].strip()
    graph = {}
    for row in input[2:]:
        first = row.split(" = ")
        second = first[1].strip()[1:-1].split(",")
        node = (second[0], second[1].strip())
        graph[first[0]] = node
        print(f"{first[0]} : {node}")

    start = "AAA"
    end = "ZZZ"
    count = 0
    current = start
    dirs = Directions(directions)
    while end != current:
        direction = dirs.get_choice()
        # print(f"{count} : {direction} {current}")
        current = graph[current][direction]
        count += 1
    print(f"RESULT: {count}")
    return count


res = run("test_08.txt", ans=2)
print()
res = run("data_08.txt")
