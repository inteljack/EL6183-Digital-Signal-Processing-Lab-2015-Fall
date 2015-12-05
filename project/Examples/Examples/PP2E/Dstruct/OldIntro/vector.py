class Vector:
    def __init__(self, start=[]):
        self.data = start

    def __add__(self, value):
        res = []
        for x in self.data: res.append(x + value)
        return Vector(res)
    __radd__ = __add__

    def __mul__(self, value):
        res = []
        for x in self.data: res.append(x * value)
        return Vector(res)
    __rmul__ = __mul__

    def sum(self, start=0):
        return reduce(lambda x,y: x + y, self.data, start)

    def prod(self, start=1):
        return reduce(lambda x,y: x * y, self.data, start)

    def __repr__(self): return `self.data`


def test():
    x = Vector([2, 4, 6])
    print x + 3, 3 + x
    print x * 4, 4 * x
    print x.sum(), x.prod()

    y = Vector([1, 2, 3])
    print x + y
    print x * y
    print x * y * 2
    print x * y * x

if __name__ == '__main__': test()    # run my self-test code
