# add subclassing and shelve class 


class Table:
    def __init__(self, mapping):
        self.proxy = mapping                 # wrap some kind of mapping

    def storeItems(self, items):             # init from dictionary
        for key in items.keys():             # do subclass __setitem__ 
            self[key] = items[key] 

    def printItems(self):                    # print wrapped mapping
        for key in self.keys():              # do subclass __getitem__
            print key, self[key]

    # defaults: to proxy
    def __getitem__(self, key):         return self.proxy[key]   
    def __setitem__(self, key, value):  self.proxy[key] = value 
    def __delitem__(self, key):         del self.proxy[key]    
    def keys(self):                     return self.proxy.keys() 


class ShelveTable(Table):                         # or use a shelve directly
    def __init__(self, mapping, fileName=None):   # since shelve works as-is
        if mapping == None:                       # could be a simple function
            import shelve             
            mapping = shelve.open(fileName)       # open file (mapping)
        self.proxy = mapping


class DbmTable(Table):
    def __init__(self, mapping, fileName=None):   # wrap table of strings
        if mapping == None:                       # can be dicts but not class
            import anydbm                         # open file (mapping)
            mapping = anydbm.open(fileName)       # unless passed-in 
        self.proxy = mapping    

    def __getitem__(self, key):                   # self.table[key]
        return eval(self.proxy[key])              # convert string to dict

    def __setitem__(self, key, value):            # self.table[key] = value
        self.proxy[key] = `value`                 # convert dict to string


class ClassTable(Table):                          # wrap table of instances
    def __init__(self, Class, mapping):           # mapping is dict or shelf
        self.Class = Class                        # save class for new
        self.proxy = mapping                      # save the real mapping

    def __getitem__(self, key):                   # make dict from instance
        instance = self.proxy[key]                # use instance dictionary
        return instance.__dict__

    def __setitem__(self, key, value):            # make instance from dict
        instance = self.Class()                   # like pickle: no init args
        for attr in value.keys():
            setattr(instance, attr, value[attr])  # set instance attributes
        self.proxy[key] = instance                # store in wrapped mapping


if __name__ == '__main__': 
    from sys import argv                          # also: formgui,formtbl tests
    from TableBrowser.formgui import FormGui      # get dict-based gui
    from formtest import Actor, cast              # get class, dict-of-dicts

    TestShelve = 'data/shelve2'                   # external file names
    TestDbm    = 'data/dbm2'
    TestType   = 'class'                          # class or dict or shelve
    TestInit   = 0                                # load file on startup?
    if len(argv) > 1: TestType = argv[1]
    if len(argv) > 2: TestInit = eval(argv[2])    
    if len(argv) > 3: TestFile = argv[3]
    else:
        TestFile = (TestType == 'shelve' and TestShelve) or TestDbm

    def load_and_go(table):
        if TestInit:                        # python formtbl2.py ?<opt> ?'-'
            table.storeItems(cast)          # (re)load cast if arg2 == 1
        FormGui( table ).mainloop()         # run gui on the table
        table.printItems()                  # tell table to print itself

    if TestType == 'class':  
        print 'dict-of-class test'
        load_and_go( ClassTable(Actor, {}) )           # map instance<->dict

    elif TestType == 'dbm':           
        print 'dbm-of-dict test'                       # open dbm file
        load_and_go( DbmTable(None, TestFile) )        # map string<->dict

    elif TestType == 'shelve':                         # just opens shelve
        print 'shelve-of-dict test'                         
        load_and_go( ShelveTable(None, TestFile+'D') )

    elif TestType == 'class-shelve':   
        print 'shelve-of-class test'
        inner = ShelveTable(None, TestFile+'C')        # open shelve file
        outer = ClassTable(Actor, inner)               # wrap it in classtable
        load_and_go( outer )
