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
    # print(f"{winning} | {users} || {golden} => {score}")
    return (score, len(golden))


def run(filename):
    history = []
    winnings = []
    with open(filename, "rt") as fp:
        sum = 0
        card_count = 0
        for n, row in enumerate(fp.readlines()):
            history.append(calc_score(row))
            winnings.append(1)

        item_count = len(winnings)
        for n, item in enumerate(history):
            score, count = item
            sum += score
            card_count += winnings[n]
            # print(f"{n}: ({score}, {count}) | {winnings[n]}")
            if count > 0:
                addition = winnings[n]
                for x in range(count):
                    pos = n + 1 + x
                    if pos < item_count:
                        winnings[pos] += addition
        print(f"Sum {sum}")
        print(f"Cards {card_count}")


run("test_04.txt")
run("data_04.txt")
