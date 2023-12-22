# import copy
import pprint
from typing import List

import common
import common_grid_coords
from common_grid_coords import Coord2, Coord3

INFINITY = 899000


class SandSlabs:
    def __init__(self, input):
        self._debug = False
        self.fall = []
        bricks = []
        self.fallen_bricks = []
        min_x = INFINITY
        min_y = INFINITY
        max_x = 0
        max_y = 0
        for num, row in enumerate(input):
            row = row.strip()
            parts = row.split("~")
            brick1 = self.get_cord3(parts[0])
            brick2 = self.get_cord3(parts[1])
            if brick1.z <= brick2.z:
                bricks.append((brick1, brick2, num))
            else:
                bricks.append((brick2, brick2, num))
            max_x = max(max_x, brick1.x, brick2.x)
            max_y = max(max_y, brick1.y, brick2.y)
            min_x = min(min_x, brick1.x, brick2.x)
            min_y = min(min_y, brick1.y, brick2.y)
        self.bricks = list(sorted(bricks, key=lambda brick: min(brick[0].z, brick[1].z)))
        self.min_coord = Coord2(min_x, min_y)
        self.max_coord = Coord2(max_x, max_y)
        self.stacks = []

    def get_cord3(self, string) -> Coord3:
        nums = string.split(",")
        return Coord3(int(nums[0]), int(nums[1]), int(nums[2]))

    def build_stacks(self, max_z=3):
        current_height = len(self.stacks)
        if current_height > max_z:
            return
        for z in range(current_height, max_z + 1):
            arr = []
            for y in range(self.max_coord.y + 1):
                arr.append([0 for _ in range(self.max_coord.x + 1)])
            self.stacks.append(arr)

    def solve(self, game_b=False) -> int:
        self.let_bricks_fall()
        return self.can_be_disintegrated()

    def let_bricks_fall(self):
        ord_a = ord("A")
        print(f"min={self.min_coord}, max={self.max_coord}")
        # for b in self.bricks:
        #     print(b)
        self.build_stacks()

        self.fall = []
        for index, brick in enumerate(self.bricks):
            brick0, brick1, num = brick
            letter = chr(ord_a + num % 28)

            diff3 = common_grid_coords.sub3(brick1, brick0)
            sign3 = common_grid_coords.sign3(diff3)
            # print(f"{index}, {letter} : {brick} |diff={diff3}  > {sign3}")
            fall_z = None
            self.build_stacks(max_z=brick0.z)
            if 1 == brick[0].z:
                # not falling
                fall_z = 0
            elif sign3.z != 0:
                # Z: fall, one square needed
                try:
                    for z in range(brick0.z - 1, 0, -1):
                        if self.stacks[z][brick0.y][brick0.x]:
                            fall_z = brick0.z - z - 1
                            # print(f"{index} falls to level z={z+1}, delta={fall_z}")
                            # print([self.stacks[z][brick0.y][brick0.x] for z in range(1, brick0.z)])
                            break
                except IndexError as ie:
                    print(f"Index Error 73: z={z} co={brick0}")
                    raise ie
                if fall_z is None:
                    print(f"{index} z falls all the way though. (fall_z is None)")
                    fall_z = brick0.z - 1
            else:
                # in x-y plane
                try_z = brick0.z - 1
                while fall_z is None and try_z >= 1:
                    plane = self.stacks[try_z]
                    co = common_grid_coords.copy3(brick0)
                    ok = 0 == plane[co.y][co.x]
                    while ok and co != brick1:
                        co = common_grid_coords.add3(co, sign3)
                        ok = 0 == plane[co.y][co.x]
                    if not ok:
                        fall_z = -1 + brick0.z - try_z
                    try_z -= 1

                if fall_z is None:
                    print(f"{index} xy falls all the way though. (fall_z is None)")
                    fall_z = brick0.z - 1

            fall_vector = Coord3(0, 0, fall_z)
            fallen0 = common_grid_coords.sub3(brick0, fall_vector)
            fallen1 = common_grid_coords.sub3(brick1, fall_vector)
            self.fallen_bricks.append((fall_z, fallen0, fallen1, sign3))

            # print(f"{index}, {letter} : fall_z={fall_z}, f0={fallen0}, {fallen1}")
            self.build_stacks(max_z=fallen1.z)

            # place brick
            co = fallen0
            fill1 = index + 1
            self.stacks[co.z][co.y][co.x] = fill1
            try:
                while co != fallen1:
                    co = common_grid_coords.add3(co, sign3)
                    self.stacks[co.z][co.y][co.x] = fill1
            except IndexError as e:
                print(f"Index Error: {co}")
                raise e
            # if index < 3:
            #     self.dump_stacks()

        fall = [f[0] for f in self.fallen_bricks]
        # print(fall)
        # self.dump_stacks()

    def can_be_disintegrated(self) -> int:
        sum1 = 0
        self.supports = {}
        self.supported_by = {}

        for index, fallen in enumerate(self.fallen_bricks):
            supports = []
            supported_by = []
            _, fallen0, fallen1, sign3 = fallen
            z1_to_check = min(fallen0.z, fallen1.z) - 1
            z2_to_check = max(fallen0.z, fallen1.z) + 1
            plane1 = self.stacks[z1_to_check]
            plane2 = self.stacks[z2_to_check]

            dest = Coord3(fallen1.x, fallen1.y, fallen0.z)
            co = common_grid_coords.copy3(fallen0)
            sign = Coord3(sign3.x, sign3.y, 0)

            v1 = plane1[co.y][co.x]
            v2 = plane2[co.y][co.x]
            supported_by.append(v1 - 1)
            supports.append(v2 - 1)
            while co != dest:
                co = common_grid_coords.add3(co, sign)
                v1 = plane1[co.y][co.x]
                v2 = plane2[co.y][co.x]
                supported_by.append(v1 - 1)
                supports.append(v2 - 1)
            self.supports[index] = set(supports)
            self.supports[index].discard(-1)
            self.supported_by[index] = set(supported_by)
            self.supported_by[index].discard(-1)

        disintegrate = []
        for index in range(len(self.fallen_bricks)):
            can_be_disintegrated1 = 1
            for other in self.supports[index]:
                if len(self.supported_by[other]) == 1:
                    can_be_disintegrated1 = 0
            disintegrate.append(can_be_disintegrated1)


        to_add_supports = []
        for key, values in self.supported_by.items():
            for value in values:
                if key not in self.supports[value]:
                    to_add_supports.append((value, key))

        to_add_supported_by = []
        for key, values in self.supports.items():
            for value in values:
                if key not in self.supported_by[value]:
                    to_add_supported_by.append((value, key))

        pprint.pprint(to_add_supports)
        print("to_add_supported_by")
        pprint.pprint(to_add_supported_by)
                    
        falling = []
        fall_count = {}
        if self._debug:
            print("==supports")
            pprint.pprint(self.supports)
            print("==supported by")
            pprint.pprint(self.supported_by)
        for index in reversed(range(len(self.fallen_bricks))):
            # print("index", index)
            if 0 == len(self.supports[index]):
                falling.append(0)
                fall_count[index] = 0
                continue
            elif disintegrate[index]:
                falling.append(0)
                fall_count[index] = 0
                continue

            to_check = set(self.supports[index])
            supported_set = set([index])
            # supported_set |= self.supports[index]
            visited = set([index])
            my_count = 0
            while len(to_check):
                supported = to_check.pop()
                if self.supported_by[supported].issubset(supported_set):
                    if supported in visited:
                        continue
                    visited.add(supported)
                    supported_set.add(supported)
                    my_count += 1
                    to_check |= self.supports[supported]
                    # print(f"{index}, {supported} , to_check={to_check}  s={supported_set}")
            falling.append(my_count)
            fall_count[index] = my_count
            
        # print(disintegrate)
        # print(list(reversed(falling)))
        for index in range(len(self.fallen_bricks)):
            print(f"{index} : {disintegrate[index]},{fall_count[index]} - {self.supported_by[index]}  >-> {self.supports[index]}")
        
        if False:
            temp = disintegrate.count(1)
            return temp
        return sum(falling)
    def dump_stacks(self):
        ord_a = ord("A") - 1

        def mod10x(n):
            return chr(ord_a + n % 25) if 0 != n else " "

        for z, plane in enumerate(self.stacks):
            print(f" ** z={z}:")
            for i, row in enumerate(plane):
                string = "".join(map(mod10x, row))
                print(f"{string} : y={i}")


def run(filename, expected=None):
    input = common.read_file_contents(filename)

    sum1 = 0
    instance = SandSlabs(input)
    sum1 = instance.solve()

    print(f"Sum is {sum1}")
    if expected is not None:
        if expected == sum1:
            print("** Correct")
        else:
            print(f"Difference, expected={expected}, actual={sum1}, diff = {sum1 - expected}")
            if abs(sum1) > 99000:
                print(f"{sum1} <= actual")
                print(f"{expected} <= expected")
    return sum1


res = run("test_22.txt", expected=7)
print()
res = run("data_22.txt")

to_high: List[int] = [
    40637,  #1
]
to_low: List[int] = [
    22275,  #2
]
if len(to_low) and res <= to_low[0]:
    print(f"Answer {res} is to low, less than {to_low[0]}")
if len(to_high) and res >= to_high[0]:
    print(f"Answer {res} is to high, less than {to_high[0]}")
