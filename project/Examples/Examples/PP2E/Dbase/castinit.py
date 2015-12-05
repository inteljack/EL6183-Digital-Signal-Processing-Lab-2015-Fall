import shelve 
from testdata import cast
db = shelve.open('data/castfile')      # create a new shelve
for key in cast.keys():
    db[key] = cast[key]                # store dictionaries in shelve
