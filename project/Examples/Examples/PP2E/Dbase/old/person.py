# a person object (data-record manager)

class Person:
    def __init__(self, name = '', job = '', pay = 0):
        self.name = name
        self.job  = job
        self.pay  = pay                 # instance ('self') data

    def basic(self):
        return self.name, self.job, self.pay

    def extra(self):                    # class methods never saved
        result = []
        for field in self.__dict__.keys():
            if field not in ['name', 'job', 'pay']:
                result.append((field, getattr(self,field)))
        return result

    def info(self): return self.basic(), self.extra()
