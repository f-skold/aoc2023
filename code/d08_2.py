import math

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


def get_nodes_ending_with(char, graph):
    nodes = []
    for key in graph.keys():
        if key.endswith(char):
            nodes.append(key)
    return set(nodes)


def handle_one_input(directions, graph, start, end):
    current_set = start
    dirs = Directions(directions)
    count = 0
    keep_working = True
    while keep_working:
        direction = dirs.get_choice()
        # print(f"{count} : {direction} {current}")
        next_states = []
        for current in current_set:
            next_states.append(graph[current][direction])
        count += 1
        current_set = set(next_states)
        outside = current_set.difference(end)
        keep_working = 0 != len(outside)
    return count


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

    start = get_nodes_ending_with("A", graph)
    end = get_nodes_ending_with("Z", graph)
    print(start)
    print(end)
    count = 0
    counts = []
    for node in start:
        counts.append(handle_one_input(directions, graph, set([node]), end))
    print(counts)
    print(math.lcm(*counts))

    # dirs = Directions(directions)
    # keep_working = True
    # while keep_working:
    #     direction = dirs.get_choice()
    #     # print(f"{count} : {direction} {current}")
    #     next_states = []
    #     for current in current_set:
    #         next_states.append(graph[current][direction])
    #     count += 1
    #     current_set = set(next_states)
    #     outside = current_set.difference(end)
    #     keep_working = (0 != len(outside))

    print(f"RESULT: {count}")
    return count


res = run("test_08_2.txt", ans=2)
print()
res = run("data_08.txt")
