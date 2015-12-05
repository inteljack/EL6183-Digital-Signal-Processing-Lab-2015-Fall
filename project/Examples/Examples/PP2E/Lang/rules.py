from string import split, join, strip

def internal_rule(string):              
    i = split(string, ' if ')         
    t = split(i[1],   ' then ')        
    r = split(i[0],   'rule ')        
    return {'rule':strip(r[1]), 'if':internal(t[0]), 'then':internal(t[1])}

def external_rule(rule):
    return ('rule '    + rule['rule']           + 
            ' if '     + external(rule['if'])   + 
            ' then '   + external(rule['then']) + '.')

def internal(conjunct):
    res = []                                    # 'a b, c d'
    for clause in split(conjunct, ','):         # -> ['a b', ' c d']
        res.append(split(clause))               # -> [['a','b'], ['c','d']]
    return res

def external(conjunct): 
    strs = []
    for clause in conjunct:                     # [['a','b'], ['c','d']] 
        strs.append(join(clause))               # -> ['a b', 'c d']    
    return join(strs, ', ')                     # -> 'a b, c d'
