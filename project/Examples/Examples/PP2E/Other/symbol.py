class Symbol:
    def __init__(self, name):           # symbol = named class instance
        self.name = name
    def __repr__(self):                 # prints as name
        return self.name
    def props(self):                    # property-list = attributes
        return self.__dict__
    def getprop(self, name):            # or just: symbol.prop
        return getattr(self, name)
    def putprop(self, name, value):     # or just: symbol.prop = value
        setattr(self, name, value)

table = {}

def intern(name):
    try:
        return table[name]              # return existing entry?
    except KeyError:
        table[name] = Symbol(name)      # else store and return new symbol
        return table[name]
