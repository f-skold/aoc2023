import common


def handle_row(row):
    return 0


def run(filename, expected=None):
    input = common.read_file_contents(filename)
    sum = 0
    for row in input:
        sum += handle_row(row.strip())
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")


res = run("test_12.txt", expected=21)
print()
res = run("data_12.txt")
