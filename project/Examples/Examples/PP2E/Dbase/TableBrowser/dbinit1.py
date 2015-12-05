######################################################################
# store a first record in a new shelve to give initial fields list;
# PyForm GUI requires an existing record before you can more records;
# delete the '?' key template record after real records are added;
# change mode, file, template to use this for other kinds of data;
# if you populate shelves from other data files you don't need this;
# see dbinit2 for object-based version, and dbview to browse shelves;
######################################################################

import os
from sys import argv
mode = 'class'
file = '../data/mydbase-' + mode
if len(argv) > 1: file = argv[1]                  # dbinit1.py file? mode??
if len(argv) > 2: mode = argv[2]
try:
    os.remove(file)                                       # delete if present
except: pass

if mode == 'dict':
    template = {'name': None, 'age': None, 'job': None}   # start dict shelve
else:
    from PP2E.Dbase.person import Person                  # one arg defaulted
    template = Person(None, None)                         # start object shelve

import shelve
dbase = shelve.open(file)                                 # create it now
dbase['?empty?'] = template 
dbase.close()
