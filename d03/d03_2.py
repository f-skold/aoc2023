import re
import math as m
import collections
from typing import Tuple

re_number = re.compile(r"([0-9]+)")

Span = collections.namedtuple("Span", ["x1", "x2"])


def is_symbol(char):
    return "." != char and not char.isdigit()


def add(x: int, tuple: Tuple[int, int]) -> Span:
    return Span(tuple[0] + x, tuple[1] + x)


class D3:
    def __init__(self, filename):
        self._do_debug = True
        with open(filename, "rt") as fp:
            self._input = list(fp.readlines())
            self._row_count = len(self._input)
            self._line_length = len(self._input[0].strip())
            print(f"{self._row_count} x {self._line_length}")

    def expand(self, span: Span) -> Span:
        return Span(max(0, span.x1 - 1), min(span.x2 + 1, self._line_length))

    def debug(self, str):
        if self._do_debug:
            print(str)

    def run(self):
        self.debug("** New run")
        sum = 0

        for y, row in enumerate(self._input):
            x = 0
            done = True
            while done:
                # self.debug(f"Searching y={y}, x={x}")
                match = re_number.search(row[x:])
                done = bool(match)
                if match:
                    size = len(match.group(1))
                    num = int(match.group(1))
                    span = match.span(0)
                    span1 = add(x, span)
                    found = 0
                    if span1.x1 > 0 and is_symbol(row[span1.x1 - 1]):
                        found = 1
                        self.debug(f"Found {found}: {row[span1.x1 - 1]}")
                    elif span1.x2 < self._line_length and is_symbol(row[span1.x2]):
                        found = 2
                    else:
                        span2 = self.expand(span1)
                        local = self.check(y - 1, span2)
                        if local:
                            found = 3
                        else:
                            local = self.check(y + 1, span2)
                            if local:
                                found = 4

                    self.debug(f"y={y}, {num} of size {size}, x={x}, {span1} => Found={found}")
                    if found:
                        sum += num
                    # len(match.group())
                    x += span[1]
                    # self.debug(f"New x={x}")
                else:
                    continue
                    pass
        print(f"Sum={sum}")
        return sum

    def check(self, y: int, span: Span):
        if y < 0 or y >= self._row_count:
            return False
        row = self._input[y]
        for xp in range(span.x1, span.x2):
            if is_symbol(row[xp]):
                return True
        return False

    def check1(self, y, start, end):
        if y < 0 or y >= self._row_count:
            return False
        row = self._input[y]
        start1 = max(0, start - 1)
        end1 = min(self._line_length, end + 1)
        for xp in range(start1, end1):
            if "." != row[xp] and not row[xp].isdigit():
                return True
        return False


if False:
    apa = "123abc567"
    for i in range(1, 4):
        print(f"{i}: {apa[i]}")

obj1 = D3("test_03.txt")
obj1.run()
if True:
    # 562569 to high
    obj2 = D3("data_03.txt")
    obj2.run()


def elses():
    board = list(open("data_03.txt"))
    chars = {(r, c): [] for r in range(140) for c in range(140) if board[r][c] not in "01234566789."}

    for r, row in enumerate(board):
        for n in re.finditer(r"\d+", row):
            edge = {(r, c) for r in (r - 1, r, r + 1) for c in range(n.start() - 1, n.end() + 1)}

            for o in edge & chars.keys():
                chars[o].append(int(n.group()))

    print(
        sum(sum(p) for p in chars.values()),
        sum(m.prod(p) for p in chars.values() if len(p) == 2),
    )


elses()
