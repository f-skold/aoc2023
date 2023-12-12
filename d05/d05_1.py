def transform(maps, num):
    for map in maps:
        start = map[0]
        diff = num - start
        if 0 <= diff and diff < map[1]:
            return diff + map[2]
    return num


class D5:
    def __init__(self, lines):
        self.maps = {}
        self.mappings = []
        self.parse(lines)

    def parse(self, lines):
        seeds_row = lines[0]
        numbers = seeds_row.split(":")
        self.seeds = [int(n) for n in numbers[1].strip().split(" ")]
        current_map = []
        current_map_name = None
        mappings = []
        maps = {}
        for line_no, row in enumerate(lines):
            if 0 == line_no:
                continue
            stripped_row = row.strip()
            if not len(stripped_row):
                continue
            if ":" == stripped_row[-1]:
                if current_map is not None:
                    maps[current_map_name] = current_map
                    mappings.append(current_map_name)
                    current_map = []
                current_map_name = stripped_row
                continue

            numbers = [int(n) for n in stripped_row.strip().split(" ")]
            # print(numbers)
            transform = (numbers[1], numbers[2], numbers[0])
            current_map.append(transform)

        maps[current_map_name] = current_map
        mappings.append(current_map_name)
        self.maps = maps
        self.mappings = mappings

    def find_lowest_location(self):
        lowest_location = 2**32
        for s in self.mappings:
            print(s)

        for seed in self.seeds:
            seed_history = [seed]
            num = seed
            for mapping in self.mappings:
                num = transform(self.maps[mapping], num)
                seed_history.append(num)
            lowest_location = min(lowest_location, num)
            # print(seed_history)
        print(f"Lowest location {lowest_location}")


def run(filename):
    with open(filename, "rt") as fp:
        d5 = D5(fp.readlines())
        d5.find_lowest_location()


run("test_05.txt")
run("data_05.txt")
