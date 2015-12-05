def permute(list):
    if not list:                                        # shuffle any sequence
        return [list]                                   # empty sequence
    else:
        res = []
        for i in range(len(list)):
            rest = list[:i] + list[i+1:]                # delete current node
            for x in permute(rest):                     # permute the others
                res.append(list[i:i+1] + x)             # add node at front
        return res


def subset(list, size):
    if size == 0 or not list:                            # order matters here
        return [list[:0]]                                # an empty sequence
    else:
        result = []
        for i in range(len(list)):
            pick = list[i:i+1]                           # sequence slice
            rest = list[:i] + list[i+1:]                 # keep [:i] part
            for x in subset(rest, size-1):
                result.append(pick + x)
        return result


def combo(list, size):
    if size == 0 or not list:                            # order doesn't matter
        return [list[:0]]                                # xyz == yzx
    else:
        result = []
        for i in range(0, (len(list) - size) + 1):       # iff enough left
            pick = list[i:i+1] 
            rest = list[i+1:]                            # drop [:i] part
            for x in combo(rest, size - 1):
                result.append(pick + x)
        return result
