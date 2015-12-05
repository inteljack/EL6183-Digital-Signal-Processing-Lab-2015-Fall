class RSequence:
    def __init__(self, object):
        self.proxy = object
    def __getattr__(self, name):
        return getattr(self.proxy, name)   # route to real object 
    def __getitem__(self, index):
        return self.proxy[index]           # intercept operators too
    def reverse(self):
        res = self.proxy[:0]
        for i in range(len(self.proxy)):   # slice and concat object
            res = self.proxy[i:i+1] + res
        return RSequence(res)
