   def intersect(self, other):
       res = {}
       for x in other:               # store other's items
           res[x] = 1
       for x in self.data:
           if res.has_key(x):        # store mine, count=2
               res[x] = 2
       for x in res.keys():
           if res[x] == 1:           # scan dict, save 2's
               del res[x]
       return Set(res.keys())
