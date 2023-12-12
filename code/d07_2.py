import copy
import collections
from enum import Enum

import common

Classification = Enum(
    "Classification",
    [
        "FIVE_OF_A_KIND",
        "FOUR_OF_A_KIND",
        "FULL_HOUSE",
        "THREE_OF_A_KIND",
        "TWO_PAIRS",
        "ONE_PAIR",
        "HIGH_CARD",
        "NONE",
    ],
)

Item = collections.namedtuple(
    "Item",
    ["val", "card_values", "classification", "raw_hand", "sorted", "counted", "bid"],
)

card_order = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
card_order2 = {c: i for i, c in enumerate(card_order)}


def sort_items(items):
    # decorated = [(item.classification, item.raw_hand, item) for item in items]
    return sorted(items)


class D7Poker:
    def __init__(self):
        pass

    def inject(self, input):
        items = []
        for row in input:
            temp = row.split(" ")
            raw_hand = temp[0]
            hand = sorted([c for c in raw_hand])
            bid = int(temp[1].strip())
            classification, counted1 = self.classify(hand)
            counted2 = []
            for i in range(5, 0, -1):
                if i in counted1:
                    if len(counted1[i]) == 1:
                        c = counted1[i][0]
                        if c.isdigit():
                            c = int(c)
                        counted2.append((i, c))
                    else:
                        counted2.append((i, "".join(counted1[i])))
            hand = "".join(hand)
            item = Item(
                classification.value,
                [card_order2[c] for c in raw_hand],
                classification,
                raw_hand,
                hand,
                counted2,
                bid,
            )
            # print(f"bid={bid}: hand={hand} : {classification}")
            print(f"raw={raw_hand}  {hand}, {classification.name:17} {counted2}: bid={bid}")
            items.append(item)
        items2 = sort_items(items)
        count = len(items2)
        result = 0
        for ix, item in enumerate(items2):
            result += item.bid * (count - ix)
        print(f"Result: {result}")
        return result

    def classify(self, cards):
        count = collections.defaultdict(int)
        for card in cards:
            count[card] += 1

        jokers = count["J"]
        highest_count = 0
        counted0 = collections.defaultdict(list)
        for card, num in count.items():
            counted0[num].append(card)
            if highest_count < num:
                highest_count = num
        classification = Classification.NONE
        jacks_highest = counted0[highest_count] == ["J"]
        counted = copy.deepcopy(counted0)
        if jacks_highest:
            if highest_count in [4, 5]:
                # To avoid 5 + 1 unhandled
                return (Classification.FIVE_OF_A_KIND, counted0)
            elif 3 == highest_count:
                if 2 in counted0:
                    return (Classification.FIVE_OF_A_KIND, counted0)
            jokers = 1
        elif len(counted[highest_count]) >= 2 and "J" in counted[highest_count]:
            counted[highest_count] = filter(lambda c: "J" != c, counted[highest_count])

        match highest_count + jokers:
            case 5:
                classification = Classification.FIVE_OF_A_KIND
            case 4:
                classification = Classification.FOUR_OF_A_KIND
            case 3:
                classification = Classification.THREE_OF_A_KIND
                if 2 == jokers:
                    # Not 4 of a kind 2J + 2X
                    pass
                elif (1 == jokers) and (2 in counted and 2 == len(counted[2])):
                    classification = Classification.FULL_HOUSE
                elif 3 in counted and 2 in counted:
                    classification = Classification.FULL_HOUSE
            case 2:
                classification = Classification.ONE_PAIR
                if 2 in counted and (len(counted[2]) > 1 or 1 == jokers):
                    classification = Classification.TWO_PAIRS
            case 1:
                classification = Classification.HIGH_CARD
        return (classification, counted0)


def run(filename, ans=None):
    input = common.read_file_contents(filename)
    d7 = D7Poker()
    result = d7.inject(input)
    if (ans is not None) and ans != result:
        print(f"ERROR: actual={result}  != {ans} (expected)")
    return result


res = run("test_07.txt", ans=5905)
print()
res = run("data_07.txt")

too_high_part_2 = [
    251856739,  # 1
    251881832,  # 3
    251897002,  # 2
    251957270,  # 4
]
if too_high_part_2 != sorted(too_high_part_2):
    print("NOTE: too_high_part_2 is not sorted")
if res >= too_high_part_2[0]:
    extra = "NEW value"
    if res in too_high_part_2:
        extra = "Occured before"
    print(f"WRONG: Res {res} >= {too_high_part_2[0]}: {extra}")

# 1: first try:
# 250422477, to low

# 2: first
# 251856739, too hig
# 251856739
# 251881832
