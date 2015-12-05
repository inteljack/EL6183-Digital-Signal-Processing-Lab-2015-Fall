#############################################################################
# PyForm table wrapper classes and tests
# Because PyForm assumes a dictionary-of-dictionary interface, this module 
# converts strings and class instance records to and from dicts.  PyForm 
# contains the table mapping--Table is not a PyForm subclass.  Note that 
# some of the wrapper classes may be useful outside PyForm--DmbOfString can
# wrap a dbm containing arbitrary datatypes.  Run the dbinit scripts to
# start a new database from scratch, and run the dbview script to browse
# a database other than the one tested here.  No longer requires classes to 
# have defaults in constructor args, and auto picks up record class from the 
# first one fetched if not passed in to class-record wrapper.  Caveat: still
# assumes that all instances in a table are instances of the same class.
############################################################################

#############################################################################
# records within tables
#############################################################################

class DictionaryRecord:
    def todict(self, value):
        return value                   # to dictionary: no need to convert 
    def fromdict(self, value):
        return value                   # from dictionary: no need to convert

class StringRecord:
    def todict(self, value):
        return eval(value)             # convert string to dictionary (or any)
    def fromdict(self, value):
        return str(value)              # convert dictionary (or any) to string

class InstanceRecord:
    def __init__(self, Class=None):    # need class object to make instances
        self.Class = Class
    def todict(self, value):           # convert instance to attr dictionary
        if not self.Class:             # get class from obj if not yet known
            self.Class = value.__class__
        return value.__dict__ 
    def fromdict(self, value):         # convert attr dictionary to instance
        try:
            class Dummy: pass                       # try what new pickle does
            instance = Dummy()                      # fails in restricted mode
            instance.__class__ = self.Class
        except:                                     # else call class, no args
            instance = self.Class()                 # init args need defaults
        for attr in value.keys():
            setattr(instance, attr, value[attr])    # set instance attributes
        return instance                             # may run Class.__setattr__

#############################################################################
# table containing records
#############################################################################

class Table:
    def __init__(self, mapping, converter):    # table object, record converter
        self.table  = mapping                  # wrap arbitrary table mapping
        self.record = converter                # wrap arbitrary record types

    def storeItems(self, items):               # initialize from dictionary
        for key in items.keys():               # do __setitem__ to xlate, store 
            self[key] = items[key]

    def printItems(self):                      # print wrapped mapping
        for key in self.keys():                # do self.keys to get table keys
            print key, self[key]               # do __getitem__ to fetch, xlate

    def __getitem__(self, key):                # on tbl[key] index fetch
        rawval = self.table[key]               # fetch from table mapping 
        return self.record.todict(rawval)      # translate to dictionary

    def __setitem__(self, key, value):         # on tbl[key]=val index assign
        rawval = self.record.fromdict(value)   # translate from dictionary
        self.table[key] = rawval               # store in table mapping

    def __delitem__(self, key):                # delete from table mapping
        del self.table[key]    

    def keys(self):                            # get table mapping keys index
        return self.table.keys()

    def close(self):
        if hasattr(self.table, 'close'):       # call table close if has one
            self.table.close()                 # may need for shelves, dbm 

#############################################################################
# table/record combinations
#############################################################################

import shelve, anydbm

def ShelveOfInstance(filename, Class=None):
    return Table(shelve.open(filename), InstanceRecord(Class))
def ShelveOfDictionary(filename):
    return Table(shelve.open(filename), DictionaryRecord())
def ShelveOfString(filename):
    return Table(shelve.open(filename), StringRecord())

def DbmOfString(filename):
    return Table(anydbm.open(filename, 'c'), StringRecord())

def DictOfInstance(dict, Class=None):
    return Table(dict, InstanceRecord(Class))
def DictOfDictionary(dict):
    return Table(dict, DictionaryRecord())
def DictOfString(filename):
    return Table(dict, StringRecord())

ObjectOfInstance   = DictOfInstance           # other mapping objects
ObjectOfDictionary = DictOfDictionary         # classes that look like dicts
ObjectOfString     = DictOfString

#############################################################################
# test common applications
#############################################################################

if __name__ == '__main__':
    from sys import argv
    from formgui import FormGui                    # get dict-based gui
    from PP2E.Dbase.testdata import Actor, cast    # get class, dict-of-dicts

    TestType   = 'shelve'                          # shelve, dbm, dict
    TestInit   = 0                                 # init file on startup?
    TestFile   = '../data/shelve1'                 # external filename
    if len(argv) > 1: TestType = argv[1]
    if len(argv) > 2: TestInit = int(argv[2])
    if len(argv) > 3: TestFile = argv[3]

    if TestType == 'shelve':                       # python formtbl.py shelve?
        print 'shelve-of-instance test'
        table = ShelveOfInstance(TestFile, Actor)  # wrap shelf in Table object
        if TestInit:
            table.storeItems(cast)                 # python formtbl.py shelve 1
        FormGui(table).mainloop()
        table.close()
        ShelveOfInstance(TestFile).printItems()    # class picked up on fetch

    elif TestType == 'dbm':                        # python formtbl.py dbm
        print 'dbm-of-dictstring test'
        table = DbmOfString(TestFile)              # wrap dbm in Table object   
        if TestInit:                               
            table.storeItems(cast)                 # python formtbl.py dbm 1
        FormGui(table).mainloop()
        table.close()
        DbmOfString(TestFile).printItems()         # dump new table contents
