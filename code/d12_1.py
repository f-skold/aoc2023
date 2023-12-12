import copy
import collections
from typing import Dict

import common

max_unknows: Dict[int, int] = collections.defaultdict(int)


def reduce(nums, run_lenghts):
    first = run_lenghts[0]
    if "." == first[0]:
        del run_lenghts[0]
    if "." == run_lenghts[-1][0]:
        del run_lenghts[-1]


def create_run_length(seq):
    run_lenghts = []
    pos = 0
    prev_char = seq[0]
    for i, char in enumerate(seq):
        if char == prev_char:
            continue
        run_lenghts.append((prev_char, i - pos))
        prev_char = char
        pos = i
    run_lenghts.append((prev_char, len(seq) - pos))
    return run_lenghts


def check_run_lengths(nums, seq1):
    rle = create_run_length(seq1)
    this_nums = []
    for item in rle:
        char = item[0]
        if "." == char:
            continue
        elif "#" == char:
            this_nums.append(item[1])
        else:
            print(f"Unknown char in {item}")
            return 0

    if nums != this_nums:
        # print(f"nums={nums} != {this_nums} : rle {rle}")
        return 0
    # print("ok")
    return 1


def permutate(seq):
    unknows = seq.count("?")
    s_in = [seq]
    for i in range(unknows):
        s_out = []
        for s in s_in:
            pos = s.index("?")
            a = copy.copy(s)
            a[pos] = "."
            s[pos] = "#"
            s_out.append(a)
            s_out.append(s)
        s_in = s_out
    return s_out


def handle_row(row: str) -> int:
    global max_unknows

    temp = row.split(" ")
    nums = [int(n) for n in temp[1].split(",")]
    seq_str = temp[0]
    seq = [c for c in seq_str]
    sequences = permutate(seq)
    count = 0
    for seq1 in sequences:
        count += check_run_lengths(nums, seq1)
    print(f"{row}  =>  count={count}")
    return count


def run(filename, expected=None):
    global max_unknows

    input = common.read_file_contents(filename)
    sum = 0
    for row in input:
        sum += handle_row(row.strip())
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")
    print("max_unknows historgam")
    for k, v in sorted(max_unknows.items()):
        print(f"{k:02}: {v}")


max_unknows = collections.defaultdict(int)
res = run("test_12.txt", expected=21)
print()
max_unknows = collections.defaultdict(int)
# res = run("data_12.txt")
