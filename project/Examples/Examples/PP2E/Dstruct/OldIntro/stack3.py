class Stack:
    def __init__(self):
        self.stack = []               # initialize list
    def push(self, object):
        self.stack.append(object)     # change in-place
    def pop(self):	
        top = self.stack[-1]          # top = end
        del   self.stack[-1]          # delete in-place
        return top
    def empty(self):
        return not self.stack
