# interact after each solution found

class Silent:
    def found(self, soln): return 1     # 1 means continue
    def final(self): pass 

class Interact:
    def found(self, soln):
        print 'Solution:', soln, 'length:', len(soln)
        answer = raw_input('More? ')                    # after each solution
        return  answer in ['Y', 'y', 'yes', 'Yes']
    def final(self):
        print 'No (more) solutions'                     # end of the search?

silent   = Silent()
interact = Interact()    # make one instance

class Graph:
    mode = silent
    def __init__(self, label, extra=None):
        self.name = label 
        self.data = extra                     
        self.arcs = []

    def __repr__(self): 
        return self.name

    def search(self, goal):
        Graph.solns = []
        if self.generate([self], goal):  
            self.mode.final()
        Graph.solns.sort(lambda x,y: cmp(len(x), len(y)))
        return Graph.solns

    def generate(self, path, goal):
        if self == goal:
            Graph.solns.append(path)                       
            return self.mode.found(path)                       
        else:
            for arc in self.arcs:
                if arc in path:                    
                    continue
                if not arc.generate(path + [arc], goal):
                    return 0
            return 1                              

if __name__ == '__main__': 
    for name in "ABCDEFG":                        # make objects first 
        exec "%s = Graph('%s')" % (name, name)    # label=variable-name
    
    A.arcs = [B, E, G]
    B.arcs = [C]                 # now configure their links:
    C.arcs = [D, E]              # embedded class-instance list
    D.arcs = [F]
    E.arcs = [C, F, G]
    G.arcs = [A]                 

    Graph.mode = interact        # change continue behavior
    A.search(G)
    Graph.mode = silent
    for (start, stop) in [(A,G), (G,F), (B,A), (D,A)]:  
        print start.search(stop)
