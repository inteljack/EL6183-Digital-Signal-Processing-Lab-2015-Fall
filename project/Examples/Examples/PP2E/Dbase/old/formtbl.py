###########################################################
# wrap special mappings for use in the form-browser
# convert strings and class-instances to/from dictionaries
# FormGui _contains_ a mapping: these aren't subclasses
###########################################################

class DbmTable:
    def __init__(self, mapping, fileName=None):   # wrap table of strings
        if mapping == None:                       # can be dicts but not class
            import anydbm                         # open file (mapping)
            mapping = anydbm.open(fileName)       # unless passed-in 
        self.proxy = mapping    
    def __getitem__(self, key):                   # self.table[key]
        return eval(self.proxy[key])              # convert string to dict
    def __setitem__(self, key, value):            # self.table[key] = value
        self.proxy[key] = `value`                 # convert dict to string
    def __delitem__(self, key):                   # del self.table[key]
        del self.proxy[key]                       # delete from wrapped dbm file
    def keys(self): return self.proxy.keys() 

class ClassTable:                                 # wrap table of instances
    def __init__(self, Class, mapping):           # mapping is dict or shelf
        self.Class = Class                        # save class for new
        self.proxy = mapping                      # save the real mapping
    def __getitem__(self, key):                   # make dict from instance
        instance = self.proxy[key]                # use instance dictionary
        return instance.__dict__
    def __setitem__(self, key, value):            # make instance from dict
        instance = self.Class()                   # like pickle: no init args!
        for attr in value.keys():
            setattr(instance, attr, value[attr])  # set instance attributes
        self.proxy[key] = instance                # store in wrapped mapping
    def __delitem__(self, key):                   # delete record by key
        del self.proxy[key]                       # from wrapped mapping
    def keys(self): return self.proxy.keys() 

if __name__ == '__main__': 
    from sys import argv
    from TableBrowser.formgui import FormGui      # get dict-based gui
    from formtest import Actor, cast              # get class, dict-of-dicts

    TestType   = 'shelve'            # shelve, dbm, dict
    TestInit   = 0                   # init file on startup?
    TestShelve = 'data/shelve1'      # external file names
    TestDbm    = 'data/dbm1'
    if len(argv) > 1: TestType = argv[1]
    if len(argv) > 2: TestInit = eval(argv[2])
    if len(argv) > 3: TestFile = argv[3]
    else:
        Testfile = (TestType == 'shelve' and TestShelve) or TestDbm

    if TestType == 'shelve':                      # "% python formtbl.py"
        print 'shelve-of-class test'
        import shelve
        shelf = shelve.open(TestFile)             # open external file, r|w
        table = ClassTable(Actor, shelf)          # wrap shelf in classtable
        if TestInit: 
            for key in cast.keys():               # "python formtbl.py shelve 1"
                table[key] = cast[key]            # initialize? - if arg3 == 1
        FormGui( table ).mainloop()
        shelf.close()
        shelf = shelve.open(TestFile)   
        for key in shelf.keys():
            print key, shelf[key].__dict__        # instance dictionary

    elif TestType == 'dbm':                       # "% python formtbl.py dbm"
        print 'dbm-of-dict test'
        import anydbm
        file = anydbm.open(TestFile)   
        if TestInit:                              # "% python formtbl.py dbm 1"
            for key in cast.keys():
                file[key] = `cast[key]`           # store as a string
        FormGui( DbmTable(file) ).mainloop()
        file.close()
