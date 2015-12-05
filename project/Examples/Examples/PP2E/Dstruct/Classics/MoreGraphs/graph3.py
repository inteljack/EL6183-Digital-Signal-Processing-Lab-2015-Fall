class Graph:
    def __init__(self, label, extra=None):
        self.name = label 
        self.data = extra 
        self.arcs = []

    def __repr__(self): 
        return self.name

    def satisfies(self, goal):
        return self == goal

    def order(self, path):
        return self.arcs

    def search(self, goal):
        Graph.solns = []
        self.generate([self], goal)
        Graph.solns.sort(lambda x,y: cmp(len(x), len(y)))
        return Graph.solns

    def generate(self, path, goal):
        if self.satisfies(goal):
            Graph.solns.append(path)                       
        else:
            for arc in self.order(path):
                if arc not in path:                    
                    arc.generate(path + [arc], goal)

if __name__ == '__main__': 
    for name in "ABCDEFG":                        # make objects first 
        exec "%s = Graph('%s')" % (name, name)    # label=variable-name
    
    A.arcs = [B, E, G]
    B.arcs = [C]                 # now configure their links:
    C.arcs = [D, E]              # embedded class-instance list
    D.arcs = [F]
    E.arcs = [C, F, G]
    G.arcs = [A]                 

    for (start, stop) in [(A,G), (G,F), (B,A), (D,A)]:  
        print start.search(stop)
