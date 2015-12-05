# session-3: use the new Person class 
import shelve 
dbase = shelve.open('cast')       # reopen shelve file
print dbase.keys()                # uses new Person definition

bob = dbase['bob']                # refetch bob
print bob                         # new class's __repr__
for who in bob.friends: 
    print who, who.info()         # new extra fields list
print bob.info()                  # new tax-rate applied
                                  
print dbase['emily'].info()       # refetch emily
for key in dbase.keys():
    obj = dbase[key]              # refetch objects by key
    print obj, obj.tax            # new tax is a computed member now
