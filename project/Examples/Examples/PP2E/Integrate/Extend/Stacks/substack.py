from oopstack import Stack              # get the 'stub' class (C-type wrapper)

class Substack(Stack):
    def __init__(self, start=[]):       # extend the 'new' operation
        Stack.__init__(self)            # initialize stack from any sequence
        for str in start:               # start can be another stack too
            self.push(str)
    def morestuff(self):                # add a new method
        print 'more stack stuff'
    def __getitem__(self, i):           # extend 'item' to trace accesses
        print 'accessing cell', i
        return Stack.__getitem__(self, i)
