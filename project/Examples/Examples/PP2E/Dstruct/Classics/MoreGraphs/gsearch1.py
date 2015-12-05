print 'gsearch1...'
More = lambda x: 1                           # continuation test: generate all

def search(start, goal, graph):
    solns = []
    if generate([start], goal, solns, graph):  
        More([])
    solns.sort( lambda x, y: cmp(len(x), len(y)) )     # sort by path length
    return solns

def generate(path, goal, solns, graph):
    state = path[-1]
    if state == goal:
        solns.append(path)                             # change solns in-place
        return More(path)                              # resume at prior level?
    else:
        for arc in graph[state]:
            if arc in path:                            # cycle found: skip it
                continue
            if not generate(path + [arc], goal, solns, graph):
                return 0
        return 1                                       # resume prior level

if __name__ == '__main__':
    import gtest                                
    print search('E', 'D', gtest.Graph)
