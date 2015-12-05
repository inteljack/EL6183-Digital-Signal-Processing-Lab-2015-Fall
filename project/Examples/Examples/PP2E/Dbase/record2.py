from string import upper

class Record:
    def __init__(self, args={}):                      # keys not ordered...
        for field in self.fields.keys(): 
            setattr(self, field, self.fields[field])  # start with defaults
        for key in args.keys(): 
            setattr(self, key, args[key])             # add from dictionary
    def basic(self):
        result = []
        for field in self.fields.keys():                  
            result.append((upper(field), getattr(self, field)))
        return result    
    def extra(self):
        result = []
        for attr in self.__dict__.keys():
            if not self.fields.has_key(attr):
                result.append(upper(attr), getattr(self, attr)) 
        return result
    def info(self):
        return (self.basic(), self.extra())        # collect all fields

class Person(Record):
    fields = { 'name':'', 'job':'', 'pay':0 }

class Student(Record):
    fields = { 'name':'', 'id':0, 'year':0, 'age':20 }
