class Language:
    def __init__(self, name=(), disk=0, role=[]):
        self.author = name
        self.disk   = disk
        self.role   = role

table = { 'Perl':   Language(('Wall', 'L.'),       2, 'stuff'),	
          'Tcl':    Language(('Ousterhout', 'J.'), 3, 'other-stuff'),
          'Python': Language(('van Rossum', 'G.'), 1, 'more-stuff') 
        }
