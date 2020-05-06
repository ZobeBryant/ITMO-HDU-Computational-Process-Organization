import unittest
from hypothesis import given
import hypothesis.strategies as st
from mutable import *

from immutable import ImDynamicArray

class TestImmutableDynamicArray(unittest.TestCase):
    def test_size(self):
        ida = ImDynamicArray()
        self.assertEqual(ida.size(), 0)
        ida.append(1)
        self.assertEqual(ida.size(), 1)
        ida.append(2)
        self.assertEqual(ida.size(), 2)

    def test_get_item(self):
        ida = ImDynamicArray()
        ida.append(1)
        self.assertEqual(ida.__getitem__(0), 1)

    def test_to_list(self):
        ida = ImDynamicArray()
        self.assertEqual(ida.to_list(), [])
        ida.add(1)
        self.assertEqual(ida.to_list(), [1])
        ida.add(2)
        self.assertEqual(ida.to_list(), [1, 2])

    def test_from_list(self):
        test_data = [
            [],
            [1],
            [1,2]
        ]
        for lst in test_data:
            ida = ImDynamicArray()
            ida.from_list(lst)
            self.assertEqual(ida.to_list(), lst)

    def test_map(self):
        ida = ImDynamicArray()
        ida.map(str)
        self.assertEqual(ida.to_list(), [])
        ida = ImDynamicArray()
        ida.from_list([1,2,3])
        ida.map(str)
        self.assertEqual(ida.to_list(), ["1", "2", "3"])

    def test_reduce(self):
        ida = ImDynamicArray()
        self.assertEqual(ida.reduce(lambda st, e: st + e, 0), 0)
        ida = ImDynamicArray()
        ida.from_list([1, 2, 3])
        self.assertEqual(ida.reduce(lambda st, e: st + e, 0), 6)

    def test_iter(self):
        x = [1, 2, 3]
        ida = ImDynamicArray()
        ida.from_list(x)
        tmp = []
        for e in ida.to_list():
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(ida.to_list(), tmp)
        i = iter(ImDynamicArray())
        self.assertRaises(StopIteration, lambda: next(i))

    def test_remove(self):
        x = [1, 2, 3]
        ida = ImDynamicArray()
        ida.from_list(x)
        ida.remove(2)
        self.assertEqual(ida.to_list(), [1, 3])

    def test_mconcat(self):
        x = [1, 2, 3]
        y = [4, 5, 6]
        ida = ImDynamicArray()
        B = ImDynamicArray()
        ida.from_list(x)
        B.from_list(y)
        ida.mconcat(B)
        self.assertEqual(ida.to_list(), [1, 2, 3, 4, 5, 6])

    def test_find(self):
        x = [1, 2, 4, 8]
        ida = ImDynamicArray()
        ida.from_list(x)
        index, _ = ida.find("is_even")
        self.assertEqual(index, [1, 2, 3])

    def test_filter(self):
        x = [1, 2, 4, 8, 3, 7, 9]
        ida = ImDynamicArray()
        ida.from_list(x)
        ida.filter("is_even")
        # self.assertEqual(da.to_list(), [1, 3, 7,9])
        print(ida.to_list())