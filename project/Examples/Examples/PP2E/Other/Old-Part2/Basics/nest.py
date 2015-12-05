def outer(x=10):
    global inner
    def inner(i):           # create inner in outer’s global
        print i             # ‘i’ found in my local scope
        if i: inner(i-1)    # ‘inner’ found in my global scope
    inner(x)
