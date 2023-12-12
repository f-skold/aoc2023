import pprint


def map_key_function(mapping):
    return mapping[0]


def transform(maps, num):
    for map in maps:
        start = map[0]
        diff = num - start
        if 0 <= diff and diff < map[1]:
            return diff + map[2]
    return num


def debug(str):
    print(str)
    return


def transform_range(maps, range1):
    num = range1[0]
    output = []
    for map in maps:
        m_start = map[0]
        diff = num - m_start
        if 0 <= diff and diff < map[1]:
            m_remaining_to_end = map[1] - diff
            print(f"{range1}, {map}: diff={diff}, rem={m_remaining_to_end}")
            if m_remaining_to_end >= range1[1]:
                output.append((diff + map[2], range1[1]))
                return output
            else:
                output.append((diff + map[2], m_remaining_to_end))
            num = map[0] + map[1]
            length = range1[1] - m_remaining_to_end
            range1 = (num, length)
            debug(f"Range remains: {range1}")
    output.append(range1)
    return output


class D5:
    def __init__(self, lines):
        self.maps = {}
        self.mappings = []

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
                if current_map_name is not None:
                    maps[current_map_name] = list(sorted(current_map, key=map_key_function))
                    mappings.append(current_map_name)
                    current_map = []
                current_map_name = stripped_row
                continue

            numbers = [int(n) for n in stripped_row.strip().split(" ")]
            # print(numbers)
            transform = (numbers[1], numbers[2], numbers[0])
            current_map.append(transform)

        maps[current_map_name] = list(sorted(current_map, key=map_key_function))
        mappings.append(current_map_name)
        self.maps = maps
        self.mappings = mappings

    def find_lowest_location(self):
        lowest_location = 2**32
        for mapping in self.mappings:
            print("mapping name", mapping)

        seed_ranges = []
        for seed_num in range(0, len(self.seeds), 2):
            value1 = self.seeds[seed_num]
            length = self.seeds[seed_num + 1]
            the_tuple = (value1, length)
            seed_ranges.append(the_tuple)

        for s in seed_ranges:
            print("seed range", s)

        for m in self.maps["seed-to-soil map:"]:
            pprint.pprint(m)

        ranges = seed_ranges
        for mapping in self.mappings:
            print()
            print("mapping name", mapping)
            new_ranges = []
            # seed_history = [seed]
            for range1 in ranges:
                print(f"Calling transform_range: {range1}")
                the_mapping = self.maps[mapping]
                pprint.pprint(the_mapping)
                temp = transform_range(self.maps[mapping], range1)
                print(f"temp={temp}")
                new_ranges += temp
            ranges = new_ranges
            print("ranges after")
            pprint.pprint(ranges)
        new_ranges.sort(key=map_key_function)
        lowest_location = new_ranges[0]
        # print(seed_history)
        print(f"Lowest location {lowest_location}")


def run(filename):
    with open(filename, "rt") as fp:
        d5 = D5(fp.readlines())
        d5.find_lowest_location()


run("test_05.txt")
run("data_05.txt")
