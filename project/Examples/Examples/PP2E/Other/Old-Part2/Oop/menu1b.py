class Menu:                                     # the menu superclass
    def __getattr__(self, name):                # pass off to 'menu'
        return getattr(self.menu, name)         # keys, append, sort...

    def run(self, prompt='?'):
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


class DictMenu(Menu):                           # a Menu subclass
    def __add__(self, other):
        new = DictMenu()                        # make a new instance
        new.menu = {}
        for key in self.menu.keys():  
            new.menu[key] = self.menu[key]      # copy 'self' dict
        for key in other.keys():  
            new.menu[key] = other[key]          # add other dict
        return new

    def showOptions(self):
        options = self.menu.keys()              # menu = mapping
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(self, cmd):
        return self.menu[cmd]()                 # call method/function


class ListMenu(Menu):                           # menu = nested sequences
    def __add__(self, other):
        new = ListMenu()                        # make a new instance
        new.menu = self.menu + other            # copy 'self' list
        return new                              # add other list

    def showOptions(self):
        for i in range(len(self.menu)):
            print '\t\t%d) %s' % (i, self.menu[i][0])

    def runCommand(self, cmd):
        try:
            index = eval(cmd)                   # convert string to number
        except: 
            raise IndexError
        return self.menu[index][1]()            # selected by number
