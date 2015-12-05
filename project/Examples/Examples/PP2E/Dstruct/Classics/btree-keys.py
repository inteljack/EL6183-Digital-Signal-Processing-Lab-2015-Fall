class KeyedBinaryTree:
    def __init__(self):          self.tree = EmptyNode()
    def __repr__(self):          return `self.tree`
    def lookup(self, key):       return self.tree.lookup(key)
    def insert(self, key, val):  self.tree = self.tree.insert(key, val)

class EmptyNode:
    def __repr__(self):
        return '*'
    def lookup(self, key):                               # fail at the bottom
        return None
    def insert(self, key, val):
        return BinaryNode(self, key, val, self)          # add node at bottom

class BinaryNode:
    def __init__(self, left, key, val, right):
        self.key,  self.val   = key, val
        self.left, self.right = left, right
    def lookup(self, key):
        if self.key == key:
            return self.val
        elif self.key > key:
            return self.left.lookup(key)                 # look in left
        else:
            return self.right.lookup(key)                # look in right
    def insert(self, key, val):
        if self.key == key:
            self.val = val
        elif self.key > key:
            self.left = self.left.insert(key, val)       # grow in left
        elif self.key < key:
            self.right = self.right.insert(key, val)     # grow in right
        return self
    def __repr__(self):
        return ('( %s, %s=%s, %s )' % 
                 (`self.left`, `self.key`, `self.val`, `self.right`)) 

if __name__ == '__main__':
    t = KeyedBinaryTree()
    for (key, val) in [('bbb', 1), ('aaa', 2), ('ccc', 3)]:
        t.insert(key, val)
    print t
    print t.lookup('aaa'), t.lookup('ccc')
    t.insert('ddd', 4)                       
    t.insert('aaa', 5)                       # changes key's value
    print t
