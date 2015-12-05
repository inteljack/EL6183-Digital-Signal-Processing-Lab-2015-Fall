class Menu:
    def __init__(self, start=None):             # inherited constructor
        self.menu = start or self.empty         # passed-in or default

    def __getitem__(self, index):               # on 'menu[index]', 'in'
        return self.menu[index]                 # index a wrapped menu

    def __setitem__(self, index, value):        # on 'menu[index] = value'
        self.menu[index] = value                # set a menu's key/index

    def __getattr__(self, name):                # on 'menu.other'
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
    empty = {}                                  # or extend __init__

    def __add__(self, other):                   # on 'dictmenu + other'
        new = DictMenu()                        # make a new instance
        for key in self.keys():  
            new[key] = self[key]                # copy 'self' dict
        for key in other.keys():  
            new[key] = other[key]               # add other dict
        return new

    __radd__ = __add__                   # transitive for mappings

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
    empty = []

    # def __add__(self, other):                   # on 'listmenu + other'
    #     return ListMenu(self.menu + other)      # make a new instance

    def __add__(self, other):                # on 'listmenu + other'
        new = self.menu[:]                   # copy my list
        for x in other:                      # loop over other: a menu too?
            new.append(x)                    # like DictMenu.__add__
        return ListMenu(new)                 # make a new instance

    def __radd__(self, other):               # on 'non-listmenu + listmenu'
        return ListMenu(other + self.menu)

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
