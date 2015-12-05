class Menu:
    def __init__(self, start):                  # inherited constructor
        self.menu = start                       # 'start' menu required here

    def __getitem__(self, index):               # index a wrapped menu
        return self.menu[index]                 # __getattr__ doesn't index

    def __setitem__(self, index, value):        # set a menu's key/index
        self.menu[index] = value

    def __getattr__(self, name):                # other 'menu' attributes
        return getattr(self.menu, name)         # keys, append, sort...

    def run(self, prompt='?'):                  # a 'real' method
        try:
            while 1:                            # common interactive loop
                print '\n\tMENU...'
                self.showOptions()
                command = raw_input(prompt)
                try:
                    flag = self.runCommand(command)
                except (IndexError, KeyError):
                    print "what: '%s'?" % command 
                else:
                    if flag: break
        except EOFError: pass                   # ctrl-d still exits all


class DictMenu(Menu): 
    def __init__(self, menu=None): 
        Menu.__init__(self, menu or {})         # new dict each time

    def __add__(self, other):                   # on: 'menu + other'
        new = DictMenu()                        # make a new instance
        for key in self.keys():  
            new[key] = self[key]                # copy 'self' dict
        for key in other.keys():  
            new[key] = other[key]               # add other dict
        return new

    def extend(self, other):                    # change menu in-place
        for key in other.keys():
            self[key] = other[key]              # uses __setitem__

    def showOptions(self):                      # more 'real' methods
        options = self.keys()                   # uses __getattr__
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(self, cmd): 
        return self[cmd]()                      # uses __getitem__


class ListMenu(Menu):
    def __init__(self, menu=None): 
        Menu.__init__(self, menu or [])         # new list each time

    def __add__(self, other):                   # on: 'menu + other'
        return ListMenu(self.menu + other)      # make a new instance

    def extend(self, other):                    # change menu in-place
        self.append(other)                      # uses __getattr__

    def showOptions(self):
        i = 0                                   # 'in' uses __getitem__
        for name, func in self:
            print '\t\t%d) %s' % (i, name); i=i+1

    def runCommand(self, cmd):
        try:
            index = eval(cmd)                   # convert string to number
        except: 
            raise IndexError
        return self[index][1]()                 # uses __getitem__
