Graph = {'A':  ['B', 'E', 'G'],
         'B':  ['C'],                        # a directed, cyclic graph
         'C':  ['D', 'E'],                   # stored as a dictionary
         'D':  ['F'],                        # 'key' leads-to [nodes]
         'E':  ['C', 'F', 'G'],
         'F':  [ ],
         'G':  ['A']  }	

def tests(searcher):                         # test searcher function
    print searcher('E', 'D', Graph)          # find all paths from 'E' to 'D'
    for x in ['AG', 'GF', 'BA', 'DA']:
        print x, searcher(x[0], x[1], Graph)
