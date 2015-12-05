from stack2 import Stack                    # extends imported Stack

class StackLog(Stack):                      # count pushes/pops, max-size
    pushes = pops = 0                       # shared/static class members
    def __init__(self, start=[]):           # could also be module vars
        self.maxlen = 0
        Stack.__init__(self, start)
    def push(self, object): 
        Stack.push(self, object)                    # do real push
        StackLog.pushes = StackLog.pushes + 1       # overall stats
        self.maxlen = max(self.maxlen, len(self))   # per-instance stats
    def pop(self):  
        StackLog.pops = StackLog.pops + 1           # overall counts
        return Stack.pop(self)                      # not 'self.pops': instance
    def stats(self):
        return self.maxlen, self.pushes, self.pops  # get counts from instance
