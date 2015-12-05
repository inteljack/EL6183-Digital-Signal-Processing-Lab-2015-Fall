# use paths stack instead of recursion 

def search(start, goal, graph):
    solns = generate( ([start], []), goal, graph) 
    solns.sort( lambda x, y: cmp(len(x), len(y)) )    
    return solns

def generate(paths, goal, graph):                      # returns solns list
    solns = []                                         # use a tuple-stack
    while paths:
        front, paths = paths                           # pop the top path
        state = front[-1]
        if state == goal:
            solns.append(front)                        # goal on this path
        else:
            for arc in graph[state]:                   # add all extensions
                if arc not in front:
                    paths = (front + [arc]), paths 
    return solns

if __name__ == '__main__': 
    import gtestfunc
    gtestfunc.tests(search)
