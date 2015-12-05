from gtest import batch, interactive

class GraphNode:
    def __init__(self, label, extra=None):
        self.name = label
        self.data = extra
        self.arcs = []
    def __repr__(self): 
        return self.name

for name in "ABCDEFG":                                
    exec "%s = GraphNode('%s')" % (name, name)     # make objects first    
    
A.arcs = [B, E, G]
B.arcs = [C]                   # now configure their links:
C.arcs = [D, E]                # embedded class instances list
D.arcs = [F]
E.arcs = [C, F, G]
G.arcs = [A]                 
    	
if __name__ == '__main__': 
    from sys import argv                    # script test routine
    exec "import " + argv[1]                # load a searcher module
    gsearch = eval(argv[1])                 # aliase the module name
    gsearch.More  = interactive             # change its continue function
    gsearch.search(A, G)
    gsearch.More = batch
    for (start, stop) in [(A,G), (G,F), (B,A), (D,A)]:  
        print (start, stop), gsearch.search(start, stop)

