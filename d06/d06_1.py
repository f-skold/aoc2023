def calc(item):
    time = item[0]
    record_distance = item[1]
    print(f"t={time}: record={record_distance}")

    count = 0
    for t in range(time + 1):
        speed = t
        duration = time - t
        distance = speed * duration
        if distance > record_distance:
            count += 1
    return count


def parse_line(line):
    first = line.split(":")
    second = first[1].split(" ")
    numbers = [int(x) for x in filter(lambda s: len(s) > 0, second)]
    return numbers


def work(lines):
    times = parse_line(lines[0])
    dists = parse_line(lines[1])
    print(times)
    print(dists)
    product = 1
    for item in zip(times, dists):
        num = calc(item)
        product *= num
        print(f"{item}: num, prod={product}")
    print(f"Final product={product}")


def run(filename):
    with open(filename, "rt") as fp:
        work(fp.readlines())


run("test_06.txt")
run("data_06.txt")
