def reverse(list):
    if not list:                               # empty? (not always [])
        return list                            # the same sequence type
    else:
        return reverse(list[1:]) + list[:1]    # add front item on the end

def ireverse(list):
    res = list[:0]                             # empty, of same type
    for i in range(len(list)): 
        res = list[i:i+1] + res                # add each item to front
    return res
