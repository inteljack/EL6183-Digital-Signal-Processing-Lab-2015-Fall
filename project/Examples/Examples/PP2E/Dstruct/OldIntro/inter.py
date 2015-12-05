def intersect(list1, list2):
    res = []                           # start with an empty list
    for x in list1:                    # scan the first list
        if x in list2:
            res.append(x)              # add common items to the end
    return res

def union(list1, list2):				
    res = map(None, list1)             # make a copy of list1
    for x in list2:                    # add new items in list2
        if not x in res:
            res.append(x)
    return res
