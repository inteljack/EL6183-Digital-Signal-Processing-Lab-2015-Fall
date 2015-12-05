from string import joinfields

def seqcon(seq, to):
    if to == '': 
        if type(seq) in map(type, ['', [], ()]):
            return joinfields(seq, '')
        else: 
            return joinfields(tuple(seq), '')
    if to == []: 
        return map(None, seq)
    if to == (): 
        return tuple(seq)
    raise TypeError

if __name__ == '__main__':
    print seqcon('spam', []), seqcon((1, 2, 3), [])
    print seqcon('eggs', ()), seqcon([4, 5, 6], ())
    print seqcon(['a', 'b'], ''), seqcon(('c', 'd'), '')

    class Test:
        def __init__(self, val):  self.data = val
        def __len__(self):        return len(self.data)
        def __getitem__(self, i): return self.data[i]

    print seqcon(Test("ab"),[]), seqcon(Test("cd"),()), seqcon(Test(['a']),'')
