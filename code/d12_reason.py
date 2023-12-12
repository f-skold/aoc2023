# import pdb
import copy


class Reasoning:
    def __init__(self, nums, rle):
        self.nums = nums
        self.nums_length = len(nums)
        self.rle = rle
        self.rle_length = len(rle)

    def peek_num(self, incr=1):
        if self.nums_pos + 1 < self.nums_length:
            return self.nums[self.nums_pos + incr]
        return 0

    def peek_rle_char(self, incr=1):
        if self.rle_pos + 1 < self.rle_length:
            return self.rle[self.rle_pos + incr][0]
        return "."

    def reason(self) -> int:
        self.rle_pos = 0
        self.nums_pos = 0
        try:
            ans = self.reason1()
        except IndexError as ie:
            print(f"rle_pos={self.rle_pos} / {self.rle_length}, nums_pos={self.nums_pos}  / {self.nums_length}")
            raise ie

        return ans

    def reason1(self) -> int:
        result = 1
        at_start = False

        if "." == self.rle[self.rle_pos][0]:
            self.rle_pos += 1
        wanted = self.nums[self.nums_pos]
        next_wanted = self.peek_num()
        while True:
            if self.rle_pos >= self.rle_length:
                if wanted:
                    breakpoint()
                    return 0
                if self.nums_pos >= self.nums_length:
                    if 0 == result:
                        breakpoint()
                    return result
            elif self.nums_pos >= self.nums_length:
                breakpoint()
                return 0
            rle_char = self.rle[self.rle_pos][0]
            # Can we assert that wanted > 0 here?

            if 0 == wanted and self.nums_pos + 1 < self.nums_length:
                self.nums_pos += 1
                wanted = self.nums[self.nums_pos]

            if "#" == rle_char:
                blocks = self.rle[self.rle_pos][1]
                if wanted == blocks:
                    self.rle_pos += 1
                    self.nums_pos += 1
                    if self.nums_pos == self.nums_length:
                        # all rle done?
                        if 0 == result:
                            breakpoint()
                        return result
                    wanted = self.nums[self.nums_pos]
                    at_start = False

                elif wanted < blocks:
                    # wanted, blocks
                    breakpoint()
                    return 0
                elif wanted > blocks:
                    wanted -= blocks
                    self.rle_pos += 1
                    at_start = True
                else:
                    raise Exception("#: All variants exceeded")
            elif "?" == rle_char:
                blocks = self.rle[self.rle_pos][1]
                if wanted > blocks:
                    at_start = True
                    wanted -= blocks
                    peek = self.peek_rle_char()
                    if "." == peek:
                        breakpoint()
                        return 0
                    self.rle_pos += 1
                elif wanted == blocks:
                    peek = self.peek_rle_char()
                    if "#" == peek:
                        # interpret current as ".", advance
                        self.rle_pos += 1
                    else:
                        self.rle_pos += 2
                        self.nums_pos += 1
                        if self.nums_pos == self.nums_length:
                            if 0 == result:
                                breakpoint()
                            return result
                        wanted = self.nums[self.nums_pos]
                        at_start = False

                elif wanted < blocks:
                    # Here we have a possible split
                    next_wanted = self.peek_num()
                    peek = self.peek_rle_char()
                    remaining = blocks - wanted
                    if at_start:
                        blocks -= wanted + 1
                        if blocks and "." == peek:
                            if next_wanted and next_wanted <= blocks:
                                result *= blocks - next_wanted
                            # remaining
                            # try 2 ways: start on next, advance to next rle
                            pass
                    elif "." == peek:
                        if remaining < next_wanted + 1:
                            result *= remaining + 1
                            self.rle_pos += 2
                            self.nums_pos += 1
                        else:
                            avail = remaining - 1
                            build_result = 0
                            cloned_rles = copy.copy(self.rle[self.rle_pos :])
                            cloned_rles[0] = (rle_char, avail)
                            r2 = Reasoning(self.nums[self.nums_pos + 1 :], cloned_rles)
                            build_result += r2.reason()
                            return result * build_result
                    elif "#" == peek:
                        # next_blocks = self.rle[self.rle_pos + 1][1]
                        avail = blocks - wanted - 1
                        # min_usage2 = wanted + 1 + next_wanted
                        # hardest

                else:
                    raise Exception("?: All variants exceeded")

            elif "." == rle_char:
                if wanted > 0:
                    breakpoint()
                    # self.nums_pos, self.rle_pos, self.nums, self.rle
                    # self.rle[self.rle_pos]
                    return 0
                self.rle_pos += 1

            else:
                raise Exception("rle_char: All variants exceeded")
        if 0 == result:
            breakpoint()
        return result
        pass
