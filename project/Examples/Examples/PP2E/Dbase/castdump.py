import shelve
db = shelve.open('data/castfile')      # reopen shelve
for key in db.keys():                  # show each key,value
    print key, db[key]
