class Stack:
    def __init__(self):               # when instance created
        self.stack = []               # self is the instance
    def push(self, object):
        self.stack = [object] + self.stack
    def pop(self):	
        top, self.stack = self.stack[0], self.stack[1:]
        return top
    def empty(self):
        return not self.stack	       
