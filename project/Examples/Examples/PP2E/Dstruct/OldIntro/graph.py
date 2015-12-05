class Graph:
    def __init__(self, label):
        self.name = label 
        self.arcs = []

    def __repr__(self): 
        return self.name

    def search(self, goal):
        Graph.solns = []
        self.generate([self], goal)
        Graph.solns.sort(lambda x,y: cmp(len(x), len(y)))
        return Graph.solns

    def generate(self, path, goal):
        if self == goal:
            self.solns.append(path)                       
        else:
            for arc in self.arcs:
                if arc not in path:                    
                    arc.generate(path + [arc], goal)

if __name__ == '__main__': 
    S = Graph('s')
    P = Graph('p')
    A = Graph('a')       # make nodes
    M = Graph('m')
    
    S.arcs = [P, M]      # S leads to P and M
    P.arcs = [S, M, A]   # arcs: embedded objects
    A.arcs = [M]
    print S.search(M)    # find paths from S to M
