def numbers(input_String):
    strs = [n.strip() for n in input_String.split(" ")]
    return set([int(n) for n in strs if len(n)])


def calc_score(row):
    first = row.split(":")
    first[0]
    second = first[1].split("|")
    winning = numbers(second[0].strip())
    users = numbers(second[1].strip())
    golden = winning.intersection(users)
    score = 0
    if len(golden):
        score = 2 ** (len(golden) - 1)
    print(f"{winning} | {users} || {golden} => {score}")
    return score


def run(filename):
    with open(filename, "rt") as fp:
        sum = 0
        for row in fp.readlines():
            sum += calc_score(row)
        print(sum)


run("test_04.txt")
run("data_04.txt")
