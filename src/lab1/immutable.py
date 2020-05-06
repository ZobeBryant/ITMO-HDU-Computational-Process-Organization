import ctypes


class ImDynamicArray:

    def __init__(self):
        """Create an empty array."""
        self._start = 0
        # Current Size
        self._n = 0
        # initial capacity
        self._capacity = 10
        self._A = self._make_array(self._capacity)

    def size(self):
        return  self._n

    def is_empty(self):
        return self._n == 0

    def __getitem__(self, k):
        if not 0 <= k < self._n:
            raise ValueError('invalid index')
        return self._A[k]

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()

    def _resize(self, c):
        array_b = self._make_array(c)
        for k in range(self._n):
            array_b[k] = self._A[k]
        self._A = array_b
        self._capacity = c

    def append(self, obj):
        if self._n == self._capacity:
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        self._n += 1
        for i in range(self._n):
            array_b[i] = self._A[i]
        array_b[self._n]=obj
        self._A = array_b

    def insert(self, k, value):
        if self._n == self._capacity:
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        for i in range(k):
            array_b[i] = self._A[i]
        array_b[k] = value
        for i in range(self._n, k, -1):
            array_b[i] = self._A[i-i]
        self._A = array_b
        self._n += 1

    def remove(self, value):
        for i in range(0, self._n):
            if self._A[i] == value:
                array_b = self._make_array(self._capacity)
                for j in range(i-1):
                    array_b[j] = self._A[j]
                for j in range(i, self._n - 1):
                    array_b[j] = self._A[j+1]
                self._n -= 1
                return
        raise ValueError('value not found')

    def to_list(self):
        res = []
        if self._n > 0:
            for i in range(self._n):
                res.append(self._A[i])
        return res

    def from_list(self, lst):
        if len(lst) == 0:
            return
        while self._capacity < len(lst):
            self._capacity = self._capacity * 2
        self._n = len(lst)
        array_b = self._make_array(self._capacity)
        for i in range(self._n):
            array_b[i] = lst[i]
        self._A = array_b

    def map(self,f):
        array_b = self._make_array(self._capacity)
        for i in range(self._n):
            array_b[i] = f(self._A[i])
        self._A = array_b

    def reduce(self,f,initial_state):
        state = initial_state
        for i in range(self._n):
            state = f(state,self._A[i])
        return state

    def __iter__(self):
        return self

    def __next__(self):
        if self._start <= self._n-1:
            res = self._A[self._start]
            self._start += 1
            return res
        else:
            raise StopIteration

    def mempty(self):
        return None

    def mconcat(self, B):
        while self._capacity < self._n + B._n:
            self._capacity = self._capacity * 2
        array_b = self._make_array(self._capacity)
        for i in range(self._n):
            array_b[i] = self._A[i]
        for i in range(self._n,self._n + B._n):
            array_b[self._n + i] = B._A[i]
        self._n = self.n + B._n
        self._A = array_b
        return self._A

    def is_even(self, e):
        if e % 2 == 0:
            return True

    def find(self, method):
        index = []
        value = []
        for i in range(self._n):
            if (method == 'is_even'):
                if self.is_even(self._A[i]):
                    index.append(i)
                    value.append(self._A[i])
        return index, value

    def filter(self, method):
        _, res = self.find(method)
        for i in range(len(res)):
            self.remove(res[i])
        return self._A

