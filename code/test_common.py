import unittest

import common


class TestRotate(unittest.TestCase):
    def setUp(self):
        self.matrix1 = [
            ["A0", "A1", "A2", "A3", "A4"],
            ["B0", "B1", "B2", "B3", "B4"],
            ["C0", "C1", "C2", "C3", "C4"],
            ["D0", "D1", "D2", "D3", "D4"],
        ]

    def test_clockwise(self):
        temp = common.rotate_clockwise(self.matrix1)
        expected_row0 = ["D0", "C0", "B0", "A0"]
        expected_row3 = ["D3", "C3", "B3", "A3"]
        self.assertEqual(temp[0], expected_row0)
        self.assertEqual(temp[3], expected_row3)

    def test_counter_clockwise(self):
        temp = common.rotate_counter_clockwise(self.matrix1)
        expected_row1 = ["A3", "B3", "C3", "D3"]
        self.assertEqual(temp[1], expected_row1)

    def test_two_steps(self):
        temp = common.rotate_two_steps(self.matrix1)
        expected_row0 = ["D4", "D3", "D2", "D1", "D0"]
        self.assertEqual(temp[0], expected_row0)

    def test_inverse(self):
        temp0 = self.matrix1
        temp1 = common.rotate_clockwise(temp0)
        temp2 = common.rotate_clockwise(temp1)
        temp3 = common.rotate_clockwise(temp2)

        rev2 = common.rotate_counter_clockwise(temp3)
        rev1 = common.rotate_counter_clockwise(rev2)
        rev0 = common.rotate_counter_clockwise(rev1)
        self.assertEqual(temp0, rev0)
        self.assertEqual(temp1, rev1)
        self.assertEqual(temp2, rev2)

    def test_four_times_gives_same(self):
        temp0 = self.matrix1
        temp0 = common.rotate_clockwise(temp0)
        temp0 = common.rotate_clockwise(temp0)
        temp0 = common.rotate_clockwise(temp0)
        temp0 = common.rotate_clockwise(temp0)
        self.assertEqual(self.matrix1, temp0)

        temp0 = self.matrix1
        temp0 = common.rotate_counter_clockwise(temp0)
        temp0 = common.rotate_counter_clockwise(temp0)
        temp0 = common.rotate_counter_clockwise(temp0)
        temp0 = common.rotate_counter_clockwise(temp0)
        self.assertEqual(self.matrix1, temp0)

    def test_two_times_two_gives_identity(self):
        temp0 = self.matrix1
        temp0 = common.rotate_two_steps(temp0)
        temp0 = common.rotate_two_steps(temp0)
        self.assertEqual(self.matrix1, temp0)
