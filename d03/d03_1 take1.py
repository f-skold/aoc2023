import re

re_number = re.compile(r"(\d+)")


class D3:
    def __init__(self, filename):
        self._do_debug = True
        with open(filename, "rt") as fp:
            self._input = list(fp.readlines())
            self._row_count = len(self._input)
            self._line_length = len(self._input[0])

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
                    start = x + span[0]
                    end = x + span[1]
                    found = 0
                    if start > 0 and "." != row[start - 1]:
                        found = 1
                        self.debug(f"Found {found}: {row[start - 1]}")
                    elif "." != row[end]:
                        found = 2
                    else:
                        local = self.check(y - 1, start, end)
                        if local:
                            found = 3
                        else:
                            local = self.check(y + 1, start, end)
                            if local:
                                found = 4

                    self.debug(f"y={y}, {num} of size {size}, x={x}, span={span} => Found={found}")
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

    def check(self, y, start, end):
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
