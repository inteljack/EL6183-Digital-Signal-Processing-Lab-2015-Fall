# an enhanced person class
# may be used with previously-stored Person objects

class Person:
    def __init__(self, name = '', job = '', pay = 0):
        self.name = name
        self.job  = job
        self.pay  = pay                   # real instance data

    def __getattr__(self, name):          # on undefined names
        if name == 'tax':
            return self.pay * .30         # a computed member
        else:
            raise AttributeError          # others are errors 

    def __repr__(self):                   # for printing myself
        return 'Person=>%s' % self.name 

    def basic(self):
        return self.name, self.job, self.pay, self.tax

    def extra(self):                      # collect unique members
        result = []
        for field in self.__dict__.keys():
            if field not in ['name', 'job', 'pay']:
                result.append((field, getattr(self,field)))
        return result

    def info(self): return self.basic(), self.extra()
