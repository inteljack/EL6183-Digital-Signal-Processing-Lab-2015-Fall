def tests(Graph):
    for name in "ABCDEFG":                               # make objects first
        exec "%s = Graph('%s')" % (name, name)           # label=variable-name

    A.arcs = [B, E, G]
    B.arcs = [C]                 # now configure their links:
    C.arcs = [D, E]              # embedded class-instance list
    D.arcs = [F]
    E.arcs = [C, F, G]
    G.arcs = [A]

    A.search(G)
    for (start, stop) in [(E,D), (A,G), (G,F), (B,A), (D,A)]:
        print start.search(stop)
