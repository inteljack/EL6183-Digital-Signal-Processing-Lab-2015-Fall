def sameclass(self, other):
    return (type(other) == type(self) and         # InstanceType? 
            other.__class__ == self.__class__)    # from same class?

class Stub2:
    def __init__(self, value):
        self.data = value
    def __coerce__(self, other): 
        if sameclass(self, other):        # called before add methods
            return self, other            # convert other up if needed
        else:
            return self, Stub2(other)
    def __add__(self, other):             # 'stub + other', 'stub + stub'
        return self.data + other.data     # other converted: add Stub2's
    __radd__ = __add__                    # 'other + stub': transitive

class Stub3:
    def __init__(self, value):
        self.data = value
    def __add__(self, other):
        if sameclass(self, other):
            return self.data + other.data    # add Stub3 instances
        else: 
            return self + Stub3(other)       # coerce other up and re-add
    __radd__ = __add__
