import unittest
from hypothesis import given
import hypothesis.strategies as st
from mutable import *

from DynamicArray import DynamicArray


class TestMutableDynamicArray(unittest.TestCase):
    def test_size(self):
        da=DynamicArray()
        self.assertEqual(da.size(), 0)
        da.add(1)
        self.assertEqual(da.size(), 1)
        da.add(2)
        self.assertEqual(da.size(), 2)

    # def test_is_empty(self):
    #     self.assertEqual(DynamicArray.is_empty(), True)

    def test_get_item(self):
        da=DynamicArray()
        da.add(1)
        self.assertEqual(da.__getitem__(0), 1)

    def test_to_list(self):
        da = DynamicArray()
        self.assertEqual(da.to_list(), [])
        da.add(1)
        self.assertEqual(da.to_list(), [1])
        da.add(2)
        self.assertEqual(da.to_list(), [1,2])

    def test_from_list(self):
        test_data=[
            [],
            [1],
            [1,2]
        ]
        for lst in test_data:
            da = DynamicArray()
            da.from_list(lst)
            self.assertEqual(da.to_list(), lst)
    def test_map(self):
        da = DynamicArray()
        da.map(str)
        self.assertEqual(da.to_list(), [])
        da=DynamicArray()
        da.from_list([1,2,3])
        da.map(str)
        self.assertEqual(da.to_list(), ["1","2","3"])

    def test_reduce(self):
        da=DynamicArray()
        self.assertEqual(da.reduce(lambda st, e: st + e, 0), 0)
        da = DynamicArray()
        da.from_list([1, 2, 3])
        self.assertEqual(da.reduce(lambda st, e: st + e, 0), 6)
    def test_iter(self):
        x = [1, 2, 3]
        da = DynamicArray()
        da.from_list(x)
        tmp = []
        for e in da.to_list():
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(da.to_list(), tmp)
        i = iter(DynamicArray())
        self.assertRaises(StopIteration, lambda: next(i))
    def test_remove(self):
        x = [1, 2, 3]
        da = DynamicArray()
        da.from_list(x)
        da.remove(2)
        self.assertEqual(da.to_list(),[1,3] )

    def test_mconcat(self):
        x=[1,2,3]
        y=[4,5,6]
        da=DynamicArray()
        B=DynamicArray()
        da.from_list(x)
        B.from_list(y)
        da.mconcat(B)
        self.assertEqual(da.to_list(), [1, 2,3,4,5,6])
    def test_find(self):
        x=[1,2,4,8]
        da = DynamicArray()
        da.from_list(x)
        index,_= da.find("is_even")
        self.assertEqual(index, [1,2,3])

    def test_filter(self):
        x = [1, 2, 4, 8,3,7,9]
        da = DynamicArray()
        da.from_list(x)
        da.filter("is_even")
       # self.assertEqual(da.to_list(), [1, 3, 7,9])
        print(da.to_list())