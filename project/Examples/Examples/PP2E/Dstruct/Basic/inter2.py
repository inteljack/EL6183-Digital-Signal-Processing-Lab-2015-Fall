def intersect(*args):
    res = [] 
    for x in args[0]:                  # scan the first list
        for other in args[1:]:         # for all other arguments
            if x not in other: break   # this item in each one?
        else:
            res.append(x)              # add common items to the end
    return res

def union(*args):				
    res = []
    for seq in args:                   # for all sequence-arguments
        for x in seq:                  # for all nodes in argument
            if not x in res: 
                res.append(x)          # add new items to result
    return res
