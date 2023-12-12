# Trebuche

tests = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]


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


d01_1_Trebuche(tests)

# not 55116
with open("data01_1.txt", "rt") as fp:
    # pass
    d01_1_Trebuche(list(fp.readlines()))
