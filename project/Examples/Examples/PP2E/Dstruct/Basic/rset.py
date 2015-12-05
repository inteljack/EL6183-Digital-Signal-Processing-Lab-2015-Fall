from set import Set

class RSet(Set):                                    # extends set.Set class
    def list(self):                                 # for sets of dictionaries
        print '\ntable =>'
        for x in self.data:
            for f in x.keys():
                print '['+f+']=' + `x[f]`,          # formatted table print
            print
 
    def select(self, field, value):
        result = []
        for x in self.data:                         # select tuples by field
            if x[field] == value:
                result.append(x)
        return RSet(result)                         # return RSet, not Set

    def bagof(self, expr):
        res = []
        for X in self.data:                         # run expr in my scope
            if eval(expr): res.append(X)            # 'X' is the loop var
        return RSet(res)                            #  use 'X' in expr string

    def find(self, field, cmp, value):
        return self.bagof('X['+ `field` +'] ' + cmp + ' ' + `value`) 

    def match(self, other, field):
        result = []
        for x in self.data:
            for y in other:
                if y[field] == x[field]:            # 'other' is any sequence
                    result.append(x)                # 'x' is in self's list
        return RSet(result)

    def join(self, other, field):
        result = []                                 # match plus fields union
        for x in self.data:                         # symbolic table links 
            for y in other:
                if y[field] == x[field]:
                    compos = self.copy_tuple(x)
                    for k in y.keys(): 
                        if not x.has_key(k): 
                            compos[k] = y[k]
                    result.append(compos)
        return RSet(result)

    def product(self, other):
        result = []                                  # permute tuples
        for x in self.data:                          # between two tables
            for y in other:                          # rename common fields
                compos = self.copy_tuple(x)
                for k in y.keys(): 
                    if not x.has_key(k): 
                        compos[k] = y[k]
                    else:
                        i = 1
                        while x.has_key(k + '_' + `i`): 
                            i = i+1
                        compos[k + '_' + `i`] = y[k]
                result.append(compos)
        return RSet(result)

    def project(self, fields):
        result = []
        for x in self.data:                          # pick-out fields
            tuple = {}                               # a 'vertical subset'
            for y in fields:
                if x.has_key(y):
                    tuple[y] = x[y]
            if tuple and not tuple in result:        # Set removes repeats too
                result.append(tuple)
        return RSet(result)

    def copy_tuple(self, tup):
        res = {}
        for field in tup.keys():
            res[field] = tup[field]                  # to copy dictionaries
        return res

    def input_tuple(self, fields):
        tup = {}
        for x in fields:
            valstr = raw_input(x + ' => ')           # input tuple fields
            tup[x] = eval(valstr)                    # any type: parse it
        self.data.append(tup)

    def difference(self, other):
        res = []                                     # should be in Set?
        for x in self.data:                          # requires Rset(result)
            if x not in other: res.append(x)
        return RSet(res)
