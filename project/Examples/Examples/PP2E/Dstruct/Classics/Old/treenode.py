# this almost works, but btree would have to return value, not 1|None

class Value:
    def __init__(self, key, value):
        self.key, self.value = key, value
    def __cmp__(self, other):
        return cmp(self.key, other.key)
    def __repr__(self): 
        return '[%s=%s]' % (self.key, self.value)

class Key:
    def __init__(self, key): self.key = key

if __name__ == '__main__':
    import btree
    tree = btree.BinaryTree()
    for (key, val) in (('bob', 1), ('ann', 2), ('cam', 3)):
        tree.insert(Value(key, val))
    print tree
    print tree.lookup(Key('cam'))    # use .val for value

