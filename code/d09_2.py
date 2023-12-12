import common


def estimate(row):
    strings = row.split(" ")
    numbers = [int(i) for i in strings]
    # print()
    # print(numbers)

    current = numbers
    several_layers_of_diff = [numbers]
    non_zero_diff = True
    while non_zero_diff:
        diff = []
        prev = None
        non_zero_diff = False
        for index, value in enumerate(current):
            if prev is not None:
                current_diff = value - prev
                diff.append(current_diff)
                if 0 != current_diff:
                    non_zero_diff = True

            prev = value
        several_layers_of_diff.append(diff)
        current = diff

    # pprint.pprint(several_layers_of_diff)
    layer_count = len(several_layers_of_diff)
    sub = several_layers_of_diff[-1][0]
    for layer in range(layer_count - 2, -1, -1):
        sub = several_layers_of_diff[layer][0] - sub
    # print(sub)
    return sub


def run(filename, ans=None):
    input = common.read_file_contents(filename)
    sum = 0
    for row in input:
        sum += estimate(row)
    print(f"Sum is {sum}")


expected_tests = 2
res = run("test_09.txt", ans=expected_tests)
print()
res = run("data_09.txt")
