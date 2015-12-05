################################################################################
# App subclasses for handling simple character-based user-interaction
################################################################################

import string
from PP2E.System.App.Bases.app import App, AppError

################################################################################
# an app with a read-eval-print loop
################################################################################

class InteractiveApp(App):
    def run(self):                          # define App.run here
        while 1:
            command = self.readCommand()
            if not command: 
                break
            result = self.evalCommand(command)
            if result == 0:
                break
            self.printResult(result)
    
    def readCommand(self, prompt='?'):      # subclass hooks + App.start,stop
        try:
            return raw_input(prompt)        # or self.input.readline()[:-1]
        except:
            return None

    def printResult(self, res):    
        if res not in [1, None]:
            print res                       # or self.output.write(`res`+'\n')

    def evalCommand(self, command):  
        raise AppError, 'evalCommand must be redefined!'


################################################################################
# an interactive app with a menu
# alternative ways to handle different menu types (dict, list, class)...
################################################################################

class MenuApp(InteractiveApp):
    def readCommand(self):                      # print menu items first
        print '\n\tMENU...'                     # or: self.output.write('--\n')
        self.showOptions()                      # or: self.write(...)
        return InteractiveApp.readCommand(self, '==>')

    def evalCommand(self, cmd):
        try:
            return self.runOption(cmd)          # catch bad key or index, etc.
        except:
            print 'what? "%s"?\ntry again...' % cmd 

    def showOptions(self):  raise AppError, 'showOptions undefined!'
    def runOptions(self):   raise AppError, 'runOptions undefined!'


class MenuDictApp(MenuApp):
    def showOptions(self):
        options = self.menu.keys()              # menu = dictionary/mapping
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runOption(self, cmd):
        return self.menu[cmd]()                 # bound method or function

class MenuListApp(MenuApp):                     # menu = list/sequence
    def showOptions(self):
        for i in range(len(self.menu)):
            print '\t\t%d) %s' % (i, self.menu[i][0])

    def runOption(self, cmd):
        return self.menu[string.atoi(cmd)][1]()

class MenuClassApp(MenuApp):
    def readCommand(self):
        return self.menu.readCommand()           # pass off to menu object
