# a person object: fields + behavior
# class defined at outer level of file

class Person:
    def __init__(self, name = '', job = '', pay = 0):
        self.name = name
        self.job  = job
        self.pay  = pay                 # real instance data

    def tax(self):
        return self.pay * 0.25          # computed on demand

    def info(self):
        return self.name, self.job, self.pay, self.tax()
