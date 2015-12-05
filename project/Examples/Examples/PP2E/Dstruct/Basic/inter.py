def intersect(seq1, seq2):
    res = []                          # start with an empty list
    for x in seq1:                    # scan the first sequence
        if x in seq2:
            res.append(x)             # add common items to the end
    return res

def union(seq1, seq2):				
    res = list(seq1)                  # make a copy of seq1
    for x in seq2:                    # add new items in seq2
        if not x in res:
            res.append(x)
    return res
