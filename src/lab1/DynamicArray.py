# mutable version
import ctypes
class DynamicArray():

    def __init__(self):
        'Create an empty array.'
        self._start=0
        self._n = 0  # size
        self._capacity = 10  # 先给个10
        self._A = self._make_array(self._capacity)


    def size(self):
        return self._n

    def is_empty(self):
        return self._n == 0

    # O(1)
    def __getitem__(self, k):
        if not 0 <= k < self._n:
            raise ValueError('invalid index')
        return self._A[k]

    # O(1)
    def add(self, obj):
        if self._n == self._capacity:  # 首先要判断该容器是否放得下
            self._resize(2 * self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def _make_array(self, c):
        return (c * ctypes.py_object)()


    def _resize(self, c):
        B = self._make_array(c)
        for k in range(self._n):
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

        # O(n)

    def insert(self, k, value):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._n, k, -1):  # 从后往前一个一个往后移
            self._A[j] = self._A[j - 1]
        self._A[k] = value
        self._n += 1

    # O(n)
    def remove(self, value):
        for k in range(self._n):
            if self._A[k] == value:  # 一个个查value
                for j in range(k, self._n - 1):
                    self._A[j] = self._A[j + 1]  ##再一个个移上来
                self._A[self._n - 1] = None
                self._n -= 1
                return
        raise ValueError('value not found')

    def to_list(self):
        res=[]
        if self._n>0:
            for i in range(self._n):
                res.append(self._A[i])
        return res

    def from_list(self, lst):
        if len(lst) == 0:
            return
        for e in lst:
            self.add(e)
    def map(self,f):
        for i in range(self._n):
            self._A[i]=f(self._A[i])

    def reduce(self,f,initial_state):
        state=initial_state
        for i in range(self._n):
            state=f(state,self._A[i])
        return state
    def __iter__(self):
        return self

    def __next__(self):

        if self._start<=self._n-1:
            res = self._A[self._start]
            self._start+=1
            return res
        else:
            raise  StopIteration

    def mempty(self):
        return None

    def mconcat(self,B):
        if B._n>0:
            for i in range(B._n):
                self.add(B._A[i])
        return self._A
    def is_even(self,e):
        if e % 2==0:
            return True


    def find(self,method):
        index=[]
        value=[]
        for i in range(self._n):
            if(method=='is_even'):
                if self.is_even(self._A[i]):
                    index.append(i)
                    value.append(self._A[i])
        return index,value

    def filter(self,method):
        _,res=self.find(method)
        for i in range(len(res)):
            self.remove(res[i])
        return self._A
