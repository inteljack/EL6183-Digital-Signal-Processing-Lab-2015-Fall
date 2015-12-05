# session-2: fetch objects from shelve

import shelve              
dbase = shelve.open('cast')           # reopen shelve file, same class
print dbase.keys()                    # no need to import class here

bob = dbase['bob']                    # fetch bob from shelve
print bob
for who in bob.friends:               # nested objects
    print who.name, who.info()
print bob.info()                      # name, job, pay, tax

print dbase['emily'].info()           # fetch emily
for key in dbase.keys():
    obj = dbase[key]                  # fetch objects by key
    print obj.name, obj.tax()         # tax is a called method here
