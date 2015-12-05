################################################################
# print C variables, which are available in the passed-in 
# cvar object's attributes; note that name 'cvar' is not 
# available as a global name in this module--its namespace
# is not the same as the dummy module where C assigned 'cvar'
################################################################

def dumpall_simple(cvar):
    print ('vars in Python:\taa=%d bb=%d cc=%s dd=%s ee=%f' %
                           (cvar.aa, cvar.bb, cvar.cc, cvar.dd, cvar.ee))

def dumpall_generic(cvar):
    print 'vars in Python:\t', 
    for name in ['aa', 'bb', 'cc', 'dd', 'ee']:
        print '%s=%s' % (name, getattr(cvar, name)),
    print

dumpall = dumpall_generic       # pick a dumper

