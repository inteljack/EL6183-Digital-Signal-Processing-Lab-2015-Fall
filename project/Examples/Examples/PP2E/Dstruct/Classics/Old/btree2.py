Found = 'Found'                               # jump to the 'found' handler

class BinaryTree:
    def __getitem__(self, i):                 # index tree in sorted order
        try:
            self.tree.count(0, i)
        except Found, value:
            return value                      # value found: 'i' in range
        raise IndexError                      # no exception: 'i' out-of-bounds

class BinaryNode:
    def count(self, i, n):
        k = self.left.count(i, n)             # count items in left
        if k == n:
            raise Found, self.data            # at node N: exit recursion
        else:
            return self.right.count(k+1, n)   # count items in right

class EmptyNode:
    def count(self, i, n):  return i          # don't count empty's
