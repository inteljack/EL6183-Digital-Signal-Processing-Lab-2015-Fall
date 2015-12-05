class Vector:
    def __init__(self, start=[]):
        self.data = start

    def __repr__(self): return `self.data`

    def apply(self, func):
        return Vector(map(func, self.data))

    def reduce(self, func, start=0):
        return reduce(func, self.data, start)

if __name__ == '__main__':
    x = Vector([2, 4, 6])
    print x.apply(lambda x: x + 10)
    print x.reduce(lambda x,y: x + y)
    print x.reduce(lambda x,y: x * y, 1)

#> python vector2.py
#[12, 14, 16]
#12
#48

