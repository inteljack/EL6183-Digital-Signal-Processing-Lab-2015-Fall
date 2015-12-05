class Record:
    def __init__(self, *args):                          # use varargs list
        for field, default in self.fields:              # for all common fields
            if args:                                    # defined in subclass
                setattr(self, field, args[0])
                args = args[1:]                         # assign next argument
            else:
                setattr(self, field, default)           # or take default value
    def basic(self):
        result = []
        for field, default in self.fields:              # collect common fields
            result.append((field, getattr(self, field)))
        return result    
    def extra(self):
        result = []
        for attr in self.__dict__.keys():               # collect unique fields
            for field, default in self.fields:          # or map/lambda here
                if field == attr: break
            else:
                result.append(attr, getattr(self, attr))
        return result
    def info(self):
        return (self.basic(), self.extra())             # collect all fields

class Person(Record):
    fields = [('name', ''), ('job', ''), ('pay', 0)]    # static: common fields

class Student(Record):
    fields = [('name', ''), ('id', 0), ('year', 0), ('age', 20)]
