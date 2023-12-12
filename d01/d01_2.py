# Trebuche
import re

tests = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]

tests2 = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]

re_digits = re.compile(r"one|two|three|four|five|six|seven|eight|nine")
digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def d01_1_Trebuche(input_rows):
    sum = 0
    for data in input_rows:
        # print(data)
        first_num = None
        last_num = 0
        for c in data:
            if "0" <= c and c <= "9":
                last_num = ord(c) - ord("0")
                if first_num is None:
                    first_num = last_num
        print(f"{first_num}{last_num}")
        sum += first_num * 10 + last_num
    print(f"Sum is {sum}")


def d01_2_Trebuche(input_rows):
    sum = 0
    for data in input_rows:
        # print(data)
        first_num = None
        last_num = 0
        for index, c in enumerate(data):
            match = re_digits.match(data[index:])
            if match:
                last_num = digits[match.group()]
                if first_num is None:
                    first_num = last_num
            elif "0" <= c and c <= "9":
                last_num = ord(c) - ord("0")
                if first_num is None:
                    first_num = last_num

        print(f"{first_num}{last_num}")
        sum += first_num * 10 + last_num
    print(f"Sum is {sum}")


d01_2_Trebuche(tests2)

# not 55116
if True:
    with open("data01_1.txt", "rt") as fp:
        # pass
        d01_2_Trebuche(list(fp.readlines()))
