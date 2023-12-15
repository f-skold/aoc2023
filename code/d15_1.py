import common


def hash(chunk) -> int:
    value = 0
    for char in chunk:
        ascii = ord(char)
        value += ascii
        value = (value * 17) % 256
    return value


def handle_row(row) -> int:
    chunks = row.split(",")
    value = 0
    for chunk in chunks:
        temp = hash(chunk)
        print(f"{temp:4} : {chunk}")
        value += temp
    return value


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    # row based simple problem
    sum = 0
    for row in input:
        sum += handle_row(row.strip())

    print(f"Sum is {sum}")
    if expected is not None:
        if expected == sum:
            print("** Correct")
        else:
            print(f"Diffrence, expected={expected}, actual={sum}")
    return sum


# rn=1 becomes 30.
# cm- becomes 253.
# qp=3 becomes 97.
# cm=2 becomes 47.
# qp- becomes 14.
# pc=4 becomes 180.
# ot=9 becomes 9.
# ab=5 becomes 197.
# pc- becomes 48.
# pc=6 becomes 214.
# ot=7 becomes 231.


res = run("test_15.txt", expected=1320)
print()
res = run("data_15.txt")
