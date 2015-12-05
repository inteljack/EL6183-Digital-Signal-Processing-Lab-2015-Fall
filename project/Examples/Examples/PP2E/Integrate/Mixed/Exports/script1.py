#####################################################
# C loads this file of Python code and runs it as 
# a single code string, after setting globals 'cvar' 
# (a type object) and 'cinterface' (a module object)
#####################################################

print 'in script1...'
from scripttools import dumpall               # import a Python module

dumpall(cvar)                                 # fetch/print exported C vars
print 'cvar.stats =', cvar.stats()            # #gets,#sets (includes .stats)
cvar.aa = cvar.bb                             # fetch C's bb, assign to C's aa
cvar.bb = cvar.bb ** 2                        # it's Python after fetch
cvar.cc, cvar.dd = 'spam', 'eggs'
cvar.ee = float(len(cvar.cc) + len(cvar.dd))  # len('spam') + len('eggs') = 8
print 'cvar.stats =', cvar.stats()
dumpall(cvar)

