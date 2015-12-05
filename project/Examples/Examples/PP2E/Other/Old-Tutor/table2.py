table = {
   'Perl':   {'author': ('Wall', 'L.'),       'use': ['sys'] },
   'Tcl':    {'author': ('Ousterhout', 'J.'), 'use': ['glue'] },
   'Python': {'author': ('van Rossum', 'G.'), 'use': ['rad'] }
}

table['Python']['author']	      # ('van Rossum', 'G.')
table['Perl']['author'][0]	      # 'Wall'
table['Python']['use'][0]	      # 'rad'
