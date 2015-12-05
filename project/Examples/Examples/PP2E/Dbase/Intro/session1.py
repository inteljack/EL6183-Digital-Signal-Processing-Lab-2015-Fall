# session-1: make objects, store in shelve

from person import Person                        # get original Person class
jerry = Person('jerry', 'dentist', 50000)        # make 3 new objects
bob   = Person('bob', 'psychologist', 70000)
emily = Person('emily', 'teacher', 40000)

# extra info for bob and emily
emily.age   = (35, 40)                               # nested tuple (range)
bob.friends = [Person('howard'), Person('peeper')]   # nested objects list

# inspect in-memory objects
print bob
print bob.info()                     # tuple: name, job, pay, tax
print emily.age, emily.tax()
print bob.friends[0].info()          # access nested objects

# put them in a shelve
import shelve                        # get persistence interface
dbase = shelve.open('cast')          # make a shelve (dbm) file called 'cast'
for obj in (bob, emily, jerry):      # pickle objects to shelve
    dbase[obj.name] = obj            # use their names as file keys
