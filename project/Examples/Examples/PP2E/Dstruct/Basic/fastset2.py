import set
                                        # fastset2.Set extends set.Set 
class Set(set.Set):
    def intersect(self, other):         # store as lists, use dicts
        res, tmp = {}, {}
        for x in self.data:             # convert self to dict 
            tmp[x] = None
        for x in other:                 # other: a sequence or Set
            if tmp.has_key(x):          # use hash-table lookup
                res[x] = None
        return Set(res.keys())          # a new list-based set

    def union(self, other):				
        res = {}                        # other: a sequence or Set
        for x in other:                 # scan each operand just once
            res[x] = None
        for x in self.data:
            res[x] = None 
        return Set(res.keys())	

