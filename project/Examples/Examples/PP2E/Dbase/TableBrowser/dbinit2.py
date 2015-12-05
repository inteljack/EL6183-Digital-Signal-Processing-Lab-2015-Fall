#################################################################
# this works too--based on Table objects not manual shelve ops;
# store a first record in shelve, as required by PyForm GUI;
#################################################################

from formtable import *
import sys, os

mode = 'dict'
file = '../data/mydbase-' + mode
if len(sys.argv) > 1: file = sys.argv[1]        
if len(sys.argv) > 2: mode = sys.argv[2]
try:    
    os.remove(file)
except: pass

if mode == 'dict':
    table    = ShelveOfDictionary(file)
    template = {'name': None, 'shoesize': None, 'language': 'Python'}
else:
    from PP2E.Dbase.person import Person
    table    = ShelveOfInstance(file, Person)
    template = Person(None, None).__dict__

table.storeItems({'?empty?': template})
table.close()
