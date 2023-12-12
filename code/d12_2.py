import collections
from typing import Dict

import common
import d12_thing
import d12_reason
import d12_stringeater

max_unknows: Dict[int, int] = collections.defaultdict(int)


def fivefold(nums, seq_str):
    o_nums = list(nums)
    o_str = seq_str
    for _ in range(4):
        o_nums += nums
        o_str += "?" + seq_str
    return (o_nums, o_str)


def handle_row(game_b, row: str) -> int:
    global max_unknows

    temp = row.split(" ")
    nums = [int(n) for n in temp[1].split(",")]
    seq_str = temp[0]

    if game_b:
        nums, seq_str = fivefold(nums, seq_str)

    print(f"seqs={seq_str}")
    print(f"nums={nums}")
    seq = [c for c in seq_str]
    thing = d12_thing.Thing(nums, seq)

    if False:
        rle = thing.create_run_length(seq)
        print(f"rle ={rle}")
        r = d12_reason.Reasoning(nums, rle)
        count = r.reason()
        print(f"unexpanded {row}  =>  count={count}")
        return count
    if False:
        sequences = thing.permutate(nums, seq)
        count = 0
        for seq1 in sequences:
            count += thing.check_run_lengths(nums, seq1)
    count = d12_stringeater.eat(seq_str, nums)
    print(f"unexpanded {row}  =>  count={count}")
    return count


def run(filename, game_b=False, expected=None):
    global max_unknows

    input = common.read_file_contents(filename)
    sum = 0
    for row in input:
        sum += handle_row(game_b, row.strip())
    print(f"Sum is {sum}")
    if expected is not None and expected != sum:
        print(f"Diffrence, expected={expected}, actual={sum}")
    print("max_unknows historgam")
    for k, v in sorted(max_unknows.items()):
        print(f"{k:02}: {v}")


# print(fivefold([1], ".#"))

max_unknows = collections.defaultdict(int)
res = run("test_12.txt", expected=21)
res = run("test_12.txt", expected=525152, game_b=True)
print()
max_unknows = collections.defaultdict(int)
res1 = run("data_12.txt")
print(f"Part 1: {res1}")
res2 = run("data_12.txt", game_b=True)
print(f"Part 2: {res2}")
