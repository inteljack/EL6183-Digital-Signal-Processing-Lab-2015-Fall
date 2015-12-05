# definitions for testing shelves, dbm, and formgui

cast = {
    'rob':   {'name': ('Rob', 'P'),   'job': 'writer', 'spouse': 'Laura'},
    'buddy': {'name': ('Buddy', 'S'), 'job': 'writer', 'spouse': 'Pickles'},
    'sally': {'name': ('Sally', 'R'), 'job': 'writer'},
    'laura': {'name': ('Laura', 'P'), 'spouse': 'Rob',   'kids':1},
    'milly': {'name': ('Milly', '?'), 'spouse': 'Jerry', 'kids':2},
    'mel':   {'name': ('Mel', 'C'),   'job': 'producer'},
    'alan':  {'name': ('Alan', 'B'),  'job': 'comedian'}
}

class Actor:                                       # unnested file-level class
    def __init__(self, name=(), job=''):           # no need for arg defaults, 
        self.name = name                           # for new pickler or formgui 
        self.job  = job                       
    def __setattr__(self, attr, value):            # on setattr(): validate
        if attr == 'kids' and value > 10:          # but set it regardless
            print 'validation error: kids =', value
        if attr == 'name' and type(value) != type(()):
            print 'validation error: name type =', type(value)
        self.__dict__[attr] = value                # don't trigger __setattr__

