print 'gsearch2...'
More = lambda x: 1

def search(start, goal, graph):
    solns, stopped = generate( ([start], []), goal, graph)
    if not stopped: 
        More([])
    solns.sort( lambda x, y: cmp(len(x), len(y)) )    
    return solns

def generate(paths, goal, graph):                 # returns solns list
    solns = []                                    # use a tuple-stack
    while paths:
        front, paths = paths                      # pop the top path
        state = front[-1]
        if state == goal:
            solns.append(front)                   # goal on this path
            if not More(front): 
                return solns, 1
        else:
            for arc in graph[state]:              # add all extensions
                if arc not in front:
                    paths = (front + [arc]), paths 
    return solns, 0

if __name__ == '__main__': 
    import gtest
    print search('E', 'D', gtest.Graph)
