# use exceptions to exit early 

class Silent:
    def found(self, soln): pass
    def final(self): pass 

class Interact:
    def found(self, soln):
        print 'Solution:', soln, 'length:', len(soln)
        answer = raw_input('More? ')                    # after each solution
        if answer not in ['Y', 'y', 'yes', 'Yes']:
            raise stopSearch
    def final(self):
        print 'No (more) solutions'                     # end of the search?

silent     = Silent()
interact   = Interact()    # make one instance
stopSearch = ''            # exit search fast

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
        try:
            self.generate([self], goal)
        except stopSearch:
            pass
        else:
            self.mode.final()
        Graph.solns.sort(lambda x,y: cmp(len(x), len(y)))
        return Graph.solns

    def generate(self, path, goal):
        if self == goal:
            Graph.solns.append(path)                       
            self.mode.found(path)                       
        else:
            for arc in self.arcs:
                if arc not in path:                    
                    arc.generate(path + [arc], goal)
