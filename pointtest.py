# Pointtest unit test for Point class


import unittest
from point import *


class PointTest(unittest.TestCase):
    def test(self):           # unittest calls methods begining with "test"
        p1 = Point(5, 0)
        p2 = Point(3, 4)

        # assertTrue is part of unittest
        self.assertFalse(p1 == p2)
        self.assertTrue(p1.length() == p2.length())
        self.assertFalse(p1 > p2)
        self.assertFalse(p1 < p2)
        self.assertTrue(p2.length() == 5.0, "length test failed")
        self.assertTrue(p1.length() == p2.length())


if __name__ == "__main__":
    unittest.main()
