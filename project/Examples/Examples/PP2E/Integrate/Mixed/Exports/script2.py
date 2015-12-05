print 'in script2...'
from scripttools import dumpall
cinterface.setMessage('Pending')              # use module: set C text area 

dumpall(cvar)
for s in cvar.cc, cvar.dd:                    # print C's cc and dd
    print s
for c in cvar.cc:                             # iterate over C string
    print c
    cvar.dd = cvar.dd + c                     # concat to C string
dumpall(cvar)

