import ctypes


class ImmutableDynamicArray:

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

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()

    def append(self, obj):
        if self._size == self._capacity:
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        for i in range(self._size):
            array_b[i] = self._array[i]
        array_b[self._size] = obj
        self._size += 1
        self._array = array_b

    def insert(self, k, value):
        if self._size == self._capacity:
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        for i in range(k):
            array_b[i] = self._array[i]
        array_b[k] = value
        for i in range(self._size, k, -1):
            array_b[i] = self._array[i - i]
        self._array = array_b
        self._size += 1

    def remove(self, value):
        for i in range(0, self._size):
            if self._array[i] == value:
                array_b = self._make_array(self._capacity)
                for j in range(i):
                    array_b[j] = self._array[j]
                for j in range(i, self._size - 1):
                    array_b[j] = self._array[j + 1]
                self._array = array_b
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
        while self._capacity < len(lst):
            self._capacity = self._capacity * 2
        self._size = len(lst)
        array_b = self._make_array(self._capacity)
        for i in range(self._size):
            array_b[i] = lst[i]
        self._array = array_b

    def map(self, f):
        array_b = self._make_array(self._capacity)
        for i in range(self._size):
            array_b[i] = f(self._array[i])
        self._array = array_b

    def reduce(self, f, initial_state):
        state = initial_state
        for i in range(self._size):
            state = f(state, self._array[i])
        return state

    def __iter__(self):
        return self

    def __next__(self):
        if self._start <= self._size-1:
            res = self._array[self._start]
            self._start += 1
            return res
        else:
            raise StopIteration

    def concatenate(self, dynamic_array):
        while self._capacity < self._size + dynamic_array.size():
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        for i in range(self._size):
            array_b[i] = self._array[i]
        lst = dynamic_array.to_list()
        for i in range(self._size, self._size + dynamic_array.size()):
            array_b[i] = lst[i - self._size]
        self._size = self._size + dynamic_array.size()
        self._array = array_b
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

