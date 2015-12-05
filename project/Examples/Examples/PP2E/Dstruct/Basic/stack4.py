error = 'stack4.error'                       # when imported: local exception

class Stack:
    def __init__(self, start=[]):            # self is the instance object
        self.stack = []                      # start is any sequence: stack..
        for x in start: self.push(x) 
    def push(self, obj):                     # methods: like module + self
        self.stack.append(obj)               # top is end of list
    def pop(self):	
        if not self.stack: raise error, 'underflow'
        return self.stack.pop()              # like fetch and delete stack[-1]
    def top(self):
        if not self.stack: raise error, 'underflow'
        return self.stack[-1]
    def empty(self):
        return not self.stack                # instance.empty()
    def __len__(self): 
        return len(self.stack)               # len(instance), not instance
    def __getitem__(self, offset):     
        return self.stack[offset]            # intance[offset], in, for
    def __repr__(self): return '[Stack:%s]' % self.stack          
