class Menu:                                     # the menu superclass
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
    def showOptions(self):
        options = self.menu.keys()              # menu = mapping
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(self, cmd):
        return self.menu[cmd]()                 # call method/function


class ListMenu(Menu):                           # menu = nested sequences
    def showOptions(self):
        for i in range(len(self.menu)):
            print '\t\t%d) %s' % (i, self.menu[i][0])

    def runCommand(self, cmd):
        try:
            index = eval(cmd)                   # convert string to number
        except: 
            raise IndexError
        return self.menu[index][1]()            # selected by number