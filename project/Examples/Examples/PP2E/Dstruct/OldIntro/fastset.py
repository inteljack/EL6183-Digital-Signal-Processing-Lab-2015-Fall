import set
                                         # fastset.Set extends set.Set 
class Set(set.Set):
    def __init__(self, value = []):
        self.data = {}                   # manages a local dictionary
        self.concat(value)               # hashing: linear search times

    def intersect(self, other):
        res = {}
        for x in other:
            if self.data.has_key(x):
                res[x] = None
        return Set(res.keys())           # a new dictionary-based set

    def union(self, other):				
        res = {}
        for x in other:                  # scan each set just once
            res[x] = None
        for x in self.data.keys():
            res[x] = None
        return Set(res.keys())	

    def concat(self, value):
        for x in value: self.data[x] = None

    # inherit and, or, len
    def __getitem__(self, key):  return self.data.keys()[key] 	
    def __repr__(self):          return '<Set:' + `self.data.keys()` + '>'
