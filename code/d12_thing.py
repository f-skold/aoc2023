import copy
import collections
from typing import Dict

max_unknows: Dict[int, int] = collections.defaultdict(int)


class Thing:
    def __init__(self, nums, seq):
        self.nums = nums
        self.nums_length = len(nums)
        self.seq = seq

    def reduce(nums, run_lenghts):
        first = run_lenghts[0]
        if "." == first[0]:
            del run_lenghts[0]
        if "." == run_lenghts[-1][0]:
            del run_lenghts[-1]

    def create_run_length(self, seq):
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

    def check_run_lengths(self, nums, seq1):
        rle = self.create_run_length(seq1)
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

    def pre_check_run_lengths(self, seq) -> bool:
        nums_pos = 0
        seq_pos = 0
        prev_char = seq[0]
        required = None
        for i, char in enumerate(seq):
            current_len = i - seq_pos
            expected = self.nums[nums_pos]
            if char == prev_char:
                continue
            if "." == prev_char:
                if required:
                    return False
            elif "#" == prev_char:
                if current_len > expected:
                    return False
                elif current_len == expected:
                    nums_pos += 1
                    required = None
                    if self.nums_length <= nums_pos:
                        return True
                else:
                    required = expected - current_len
            elif "?" == prev_char:
                return not required or current_len >= required

            prev_char = char
            seq_pos = i

        return True

    def permutate(self, nums, seq):
        unknows = seq.count("?")
        s_in = [seq]
        for i in range(unknows):
            s_out = []
            if 0 == (i % 10) or i == unknows - 1:
                print(f"{i}/{unknows} > {len(s_in)}")
            for s in s_in:
                pos = s.index("?")
                a = copy.copy(s)
                a[pos] = "."
                s[pos] = "#"
                t1 = self.pre_check_run_lengths(a)
                # print(f"{i} . : {''.join(a)} : {t1}")
                if t1:
                    s_out.append(a)
                t2 = self.pre_check_run_lengths(s)
                # print(f"{i} # : {''.join(s)} : {t2}")
                if t2:
                    s_out.append(s)
            s_in = s_out
        return s_out
