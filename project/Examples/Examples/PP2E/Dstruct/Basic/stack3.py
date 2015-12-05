class Stack:
    def __init__(self, start=[]):              # init from any sequence
        self.stack = None                      # even other (fast)stacks
        for i in range(-len(start), 0): 
            self.push(start[-i - 1])           # push in reverse order
    def push(self, node):                      # grow tree 'up/left'
        self.stack = node, self.stack          # new root tuple: (node, tree)
    def pop(self): 
        node, self.stack = self.stack          # remove root tuple
        return node                            # TypeError if empty
    def empty(self): 
        return not self.stack                  # is it 'None'?
    def __len__(self):                         # on: len, not
        len, tree = 0, self.stack
        while tree:
            len, tree = len+1, tree[1]         # visit right subtrees
        return len
    def __getitem__(self, index):              # on: x[i], in, for
        len, tree = 0, self.stack
        while len < index and tree:            # visit/count nodes
            len, tree = len+1, tree[1] 
        if tree:
            return tree[0]                     # IndexError if out-of-bounds
        else: raise IndexError                 # so 'in' and 'for' stop
    def __repr__(self): return '[FastStack:' + `self.stack` + ']' 
