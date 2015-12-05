Graph = {'A':  ['B', 'E', 'G'],
         'B':  ['C'],                     # a directed, cyclic graph
         'C':  ['D', 'E'],                # stored as a dictionary
         'D':  ['F'],                     # 'key' leads-to [nodes]
         'E':  ['C', 'F', 'G'],
         'F':  [ ],
         'G':  ['A']  }	
    	
def batch(soln): 
    if soln:  return 1                                  # generate all paths

def interactive(soln):
    if not soln:
        print 'No (more) solutions'                     # end of the search?
    else: 
        print 'Solution:', soln, 'length:', len(soln)	
        answer = raw_input('More? ')                    # after each solution
        return  answer in ['Y', 'y', 'yes', 'Yes']

if __name__ == '__main__': 
    from sys import argv                    # script test routine
    exec "import " + argv[1]                # load a searcher module
    gsearch = eval(argv[1])                 # aliase the module name
    gsearch.More  = interactive             # change its continue function
    gsearch.search('A', 'G', Graph)
    gsearch.More = batch
    for x in ['AG', 'GF', 'BA', 'DA']:  
        print x, gsearch.search(x[0], x[1], Graph)
