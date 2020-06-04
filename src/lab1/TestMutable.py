# mutable version 
import unittest
from hypothesis import given
import hypothesis.strategies as st

from src.lab1.Mutable import *


class TestMutableDynamicArray(unittest.TestCase):
    def test_size(self):
        dynamic_array = MutableDynamicArray()
        self.assertEqual(dynamic_array.size(), 0)
        dynamic_array.append(1)
        self.assertEqual(dynamic_array.size(), 1)
        dynamic_array.append(2)
        self.assertEqual(dynamic_array.size(), 2)

    def test_is_empty(self):
        dynamic_array = MutableDynamicArray()
        self.assertEqual(dynamic_array.is_empty(), True)

    def test_get_item(self):
        dynamic_array=MutableDynamicArray()
        dynamic_array.append(1)
        self.assertEqual(dynamic_array.__getitem__(0), 1)

    def test_to_list(self):
        dynamic_array = MutableDynamicArray()
        self.assertEqual(dynamic_array.to_list(), [])
        dynamic_array.append(1)
        self.assertEqual(dynamic_array.to_list(), [1])
        dynamic_array.append(2)
        self.assertEqual(dynamic_array.to_list(), [1, 2])

    def test_from_list(self):
        test_data = [
            [],
            [1],
            [1, 2]
        ]
        for lst in test_data:
            dynamic_array = MutableDynamicArray()
            dynamic_array.from_list(lst)
            self.assertEqual(dynamic_array.to_list(), lst)

    def test_map(self):
        dynamic_array = MutableDynamicArray()
        dynamic_array.map(str)
        self.assertEqual(dynamic_array.to_list(), [])
        dynamic_array=MutableDynamicArray()
        dynamic_array.from_list([1, 2, 3])
        dynamic_array.map(str)
        self.assertEqual(dynamic_array.to_list(), ["1", "2", "3"])

    def test_reduce(self):
        dynamic_array = MutableDynamicArray()
        self.assertEqual(dynamic_array.reduce(lambda a, e: a + e, 0), 0)
        dynamic_array = MutableDynamicArray()
        dynamic_array.from_list([1, 2, 3])
        self.assertEqual(dynamic_array.reduce(lambda a, e: a + e, 0), 6)

    def test_iter(self):
        x = [1, 2, 3]
        dynamic_array = MutableDynamicArray()
        dynamic_array.from_list(x)
        tmp = []
        for e in dynamic_array.to_list():
            tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(dynamic_array.to_list(), tmp)
        i = iter(MutableDynamicArray())
        self.assertRaises(StopIteration, lambda: next(i))

    def test_remove(self):
        x = [1, 2, 3]
        dynamic_array = MutableDynamicArray()
        dynamic_array.from_list(x)
        dynamic_array.remove(2)
        self.assertEqual(dynamic_array.to_list(),[1,3])

    def test_concatenate(self):
        x = [1, 2, 3]
        y = [4, 5, 6]
        dynamic_array_a = MutableDynamicArray()
        dynamic_array_b = MutableDynamicArray()
        dynamic_array_a.from_list(x)
        dynamic_array_b.from_list(y)
        dynamic_array_a.concatenate(dynamic_array_b)
        self.assertEqual(dynamic_array_a.to_list(), [1, 2, 3, 4, 5, 6])

    def test_find(self):
        x = [1, 2, 4, 8]
        dynamic_array = MutableDynamicArray()
        dynamic_array.from_list(x)
        index,_= dynamic_array.find("is_even")
        self.assertEqual(index, [1, 2, 3])

    def test_filter(self):
        x = [1, 2, 4, 8, 3, 7, 9]
        dynamic_array = MutableDynamicArray()
        dynamic_array.from_list(x)
        dynamic_array.filter("is_even")
        self.assertEqual(dynamic_array.to_list(), [1, 3, 7,9])

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        array = MutableDynamicArray()
        array.from_list(a)
        b = array.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        array = MutableDynamicArray()
        array.from_list(a)
        self.assertEqual(array.size(), len(a))


if __name__ == '__main__':
    unittest.main()
