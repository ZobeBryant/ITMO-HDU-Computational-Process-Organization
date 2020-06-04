# mutable version
import ctypes


class MutableDynamicArray:

    def __init__(self):
        self._start = 0
        self._size = 0
        self._capacity = 10
        self._array = self._make_array(self._capacity)

    def size(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def __getitem__(self, k):
        if not 0 <= k < self._size:
            raise ValueError('invalid index')
        return self._array[k]

    def append(self, obj):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._array[self._size] = obj
        self._size += 1

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()

    def _resize(self, c):
        array_b = self._make_array(c)
        for k in range(self._size):
            array_b[k] = self._array[k]
        self._array = array_b
        self._capacity = c

    def insert(self, k, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._size, k, -1):
            self._array[j] = self._array[j - 1]
        self._array[k] = value
        self._size += 1

    def remove(self, value):
        for k in range(self._size):
            if self._array[k] == value:
                for j in range(k, self._size - 1):
                    self._array[j] = self._array[j + 1]
                self._array[self._size - 1] = None
                self._size -= 1
                return
        raise ValueError('value not found')

    def to_list(self):
        res = []
        if self._size > 0:
            for i in range(self._size):
                res.append(self._array[i])
        return res

    def from_list(self, lst):
        if len(lst) == 0:
            return
        for e in lst:
            self.append(e)

    def map(self, f):
        for i in range(self._size):
            self._array[i] = f(self._array[i])

    def reduce(self, f, initial_state):
        state = initial_state
        for i in range(self._size):
            state = f(state, self._array[i])
        return state

    def __iter__(self):
        return self

    def __next__(self):

        if self._start <= self._size - 1:
            res = self._array[self._start]
            self._start += 1
            return res
        else:
            raise StopIteration

    def concatenate(self, dynamic_array):
        lst = dynamic_array.to_list()
        if dynamic_array.size() > 0:
            for i in range(len(lst)):
                self.append(lst[i])
        return self._array

    @staticmethod
    def is_even(e):
        if e % 2 == 0:
            return True

    def find(self, method):
        index = []
        value = []
        for i in range(self._size):
            if method == 'is_even':
                if self.is_even(self._array[i]):
                    index.append(i)
                    value.append(self._array[i])
        return index, value

    def filter(self, method):
        _, res = self.find(method)
        for i in range(len(res)):
            self.remove(res[i])
        return self._array
