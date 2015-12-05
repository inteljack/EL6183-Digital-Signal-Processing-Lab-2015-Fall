print 'in script3...'
import sys
from scripttools import dumpall

for attr in 'aa', 'bb', 'cc', 'dd', 'ee':    # fetch C vars generically
    print attr, '=', getattr(cvar, attr)     # by attribute name string
setattr(cvar, 'cc', 'Bye')
print 'cvar.stats  =', cvar.stats()          # attribute gets, sets

try:
    cvar.xx                                  # getattr error
except:
    print sys.exc_type, sys.exc_value

try:
    cvar.xx = 'bad'                          # setattr error
except:
    print sys.exc_type, sys.exc_value

try:
    cvar.aa = 'bad'                          # type error
except:
    print sys.exc_type, sys.exc_value

try:
    cinterface.xx                            # module error
except:
    print sys.exc_type, sys.exc_value

print 'dir(cvar)   =', dir(cvar)             # just stats: rest via getattr
print 'cvar.stats  =', cvar.stats()          # attribute gets, sets
print 'sys.modules =', sys.modules.keys()    # runpy, sripttools, cinterface

import cinterface                            # this would fail if CnameMapTable
mycvar = cinterface.Cvar()                   # can't be linked to cinterface.so
print 'cvar.aa, the hard way:', mycvar.aa    # from enclosing C layer or other

cinterface.setMessage("Finished.\n")
dumpall(cvar)

