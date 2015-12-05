##################################################
# Python and C make the Cvar object defined here
# instead of a type instance in a C module file;
# backward compatible with the C type version
##################################################

import cinterfacemod                               # load C extension module
for attr in 'setMessage', 'getname', 'setname':    # debugging sanity test 
    assert hasattr(cinterfacemod, attr), attr      # check all C names used

def setMessage(text):
    cinterfacemod.setMessage(text)                 # pass off to C module

class Count:
    def __init__(self):
        self.gets = self.sets = 0                  # separate counter object
    def get(self):                                 # to avoid setattr calls
        self.gets = self.gets + 1
    def set(self):
        self.sets = self.sets + 1
    def stats(self):
        return (self.gets, self.sets)
    
class Cvar:
    def __init__(self):                            # on cinterface.Cvar()
        self.__dict__['count'] = Count()           # don't trigger setattr 

    def __getattr__(self, name):                   # on instance.name
        self.count.get()                           # undefined names only
        return cinterfacemod.getname(name)

    def __setattr__(self, name, value):            # on instance.name = value
        self.count.set()                           # every attribute assignment
        return cinterfacemod.setname(name, value)

    def __repr__(self):
        return '<Cvar object: %d, %d>' % self.count.stats()

    def stats(self):
        self.count.get()
        return self.count.stats()

