import stacktype                                # get the C type/module
class Stack:
    def __init__(self, start=None):             # make/wrap a C type-instance
        self._base = start or stacktype.Stack() # deleted when class-instance is
    def __getattr__(self, name):
        return getattr(self._base, name)        # methods/members: type-instance
    def __cmp__(self, other):
        return cmp(self._base, other)
    def __repr__(self):                         # 'print' is not really repr
        print self._base,; return ''
    def __add__(self, other):                   # operators: special methods
        return Stack(self._base + other._base)  # operators are not attributes
    def __mul__(self, n): 
        return Stack(self._base * n)            # wrap result in a new Stack
    def __getitem__(self, i): 
        return self._base[i]                    # 'item': index, in, for
    def __len__(self):
        return len(self._base)
