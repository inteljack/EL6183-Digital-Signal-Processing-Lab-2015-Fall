import interface                              # C++ handshaking module
class Stub:
    def __init__(self, object):
        self.wrapped = object
    def __add__(self, other):                 # 'Stub + other', 'Stub + Stub'
        return self.toPython() + other
    def __radd__(self, other):                # 'other + Stub'
        return other + self.toPython()
    def __getattr__(self, name):
        if name == "__coerce__":              # coerce tried before add/radd
            raise AttributeError, name        # fail: convert in add methods
        try:
            return Stub(interface.getField(self.wrapped, name)) 
        except:
            raise AttributeError, name
    def __getitem__(self, index):
        try:
            return Stub(interface.getIndex(self.wrapped, index))
        except:
            raise IndexError   # end for-loops, in-tests
    def __repr__(self):
        return "(" + `self.toPython()` + ")"
    def toPython(self):
        return interface.convertDown(self.wrapped)    # a native Python object
