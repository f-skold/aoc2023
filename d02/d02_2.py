def handle_row_power(row):
    parts = row.split(":")
    game_no = int(parts[0][5:])
    groups = parts[1].split(";")

    max_values = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for group in groups:
        blocks = group.split(",")
        for block in blocks:
            trimmed_block = block.strip()
            block_part = trimmed_block.split(" ")
            num = int(block_part[0])
            color = block_part[1]
            if num > max_values[color]:
                max_values[color] = num
    power = max_values["red"] * max_values["green"] * max_values["blue"]
    return power

    if max_values["red"] <= 12 and max_values["green"] <= 13 and max_values["blue"] <= 14:
        return game_no
    else:
        return 0


def run(filename):
    with open(filename, "rt") as fp:
        sum = 0
        for row in fp.readlines():
            sum += handle_row_power(row)
        print(sum)


run("test02.txt")
run("data_02.txt")
