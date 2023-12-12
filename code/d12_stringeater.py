from typing import Dict

memory: Dict[str, int] = {}


# memorized
def eat(text, nums) -> int:
    global memory

    key = f"{text}|{str(nums)}"
    if key in memory:
        return memory[key]
    ans = eat_inner(text, nums)
    memory[key] = ans
    return ans


def eat_inner(text, nums):
    if 0 == len(nums):
        return "#" not in text

    while len(text) and "." == text[0]:
        text = text[1:]

    if len(text) < sum(nums) + len(nums) - 1:
        return 0

    count = nums[0]
    if count == len(text):
        return "." not in text

    total = 0
    if "?" == text[0]:
        # Interpret as .
        total += eat(text[1:], nums)
    block = text[:count]
    if "." not in block and "#" != text[count]:
        total += eat(text[count + 1 :], nums[1:])
    return total
