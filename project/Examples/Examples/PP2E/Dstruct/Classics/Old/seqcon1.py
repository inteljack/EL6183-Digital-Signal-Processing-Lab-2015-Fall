class sequence:                             # don't make sequence() directly
    def __init__(self, value=[]):  
        self.data = self.empty()            # empty is virtual
        self.concat(value)

    def convert(self, Maker):
        new = Maker()
        new.concat(self.data)
        return new

    def concat(self, items):                # "in" is generic
        for x in items: self.add(x)         # add is virtual

    def to_string(self): return String(self.data)     
    def to_list(self):   return List(self.data)
    def to_tuple(self):  return Tuple(self.data)

    def __repr__(self): return `self.data`

class List(sequence):
    def empty(self):     return []  
    def add(self, item): self.data.append(item)

class String(sequence):
    def empty(self):     return ''
    def add(self, item): self.data = self.data + item
 
class Tuple(sequence):
    def empty(self):     return ()
    def add(self, item): self.data = self.data + (item,)

if __name__ == "__main__":
    x = List("spam")
    print x, x.convert(String), x.to_tuple()
    y = String("eggs")
    print y, y.convert(Tuple),  y.to_list()
