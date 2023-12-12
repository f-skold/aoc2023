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
    ],
)

Item = collections.namedtuple("Item", ["val", "card_values", "classification", "raw_hand", "bid"])

card_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
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
            classification = self.classify(hand)
            item = Item(
                classification.value,
                [card_order2[c] for c in raw_hand],
                classification,
                raw_hand,
                bid,
            )
            print(f"bid={bid}: hand={hand} : {classification} {item}")
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

        highest_count = 0
        counted = collections.defaultdict(list)
        for card, num in count.items():
            counted[num].append(card)
            if highest_count < num:
                highest_count = num
        classification = Classification.HIGH_CARD
        match highest_count:
            case 5:
                classification = Classification.FIVE_OF_A_KIND
            case 4:
                classification = Classification.FOUR_OF_A_KIND
            case 3:
                classification = Classification.THREE_OF_A_KIND
                if 2 in counted:
                    classification = Classification.FULL_HOUSE
            case 2:
                classification = Classification.ONE_PAIR
                if len(counted[2]) > 1:
                    classification = Classification.TWO_PAIRS
            case 1:
                classification = Classification.HIGH_CARD
        return classification


def run(filename, ans=None):
    input = common.read_file_contents(filename)
    d7 = D7Poker()
    result = d7.inject(input)
    if (ans is not None) and ans != result:
        print(f"ERROR: actual={result}  != {ans} (expected)")


run("test_07.txt", ans=6440)
run("data_07.txt")
# first try:
# 250422477, to low
