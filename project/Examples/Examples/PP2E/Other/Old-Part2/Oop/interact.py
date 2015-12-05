class Interact:
    def __init__(self):
        self.prompt = '?'

    def run(self):   
        while 1:
            command = self.readCommand()
            if not command: 
                break
            result = self.evalCommand(command)
            if result:
                break
    
    def readCommand(self): 
        try:
            return raw_input(self.prompt) 
        except:
            return None                         # break loop on ctrl-d


class Menu(Interact):
    def readCommand(self):                      # extend superclass read
        print '\n\tMENU...'                     # print menu items first
        self.showOptions()                     
        return Interact.readCommand(self)

    def evalCommand(self, cmd):
        try:
            return self.runCommand(cmd)         # catch bad key/index, etc.
        except (EOFError, SystemExit):          # let sys.exit, ctrl-d pass
            return 1                            # but break main loop
        except:
            print "what: '%s'?" % cmd           # return None implicitly


# the rest is exactly the same as menu1.py 
# subclasses repeated here for convenience


class DictMenu(Menu):
    def showOptions(self):
        options = self.menu.keys()              # menu = dictionary
        options.sort()
        for cmd in options: print '\t\t' + cmd

    def runCommand(self, cmd):
        return self.menu[cmd]()                 # call action by name

class ListMenu(Menu):                           # menu = nested sequences
    def showOptions(self):
        for i in range(len(self.menu)):
            print '\t\t%d) %s' % (i, self.menu[i][0])

    def runCommand(self, cmd):
        try:
            index = eval(cmd)                   # convert string to number
        except: 
            raise IndexError
        return self.menu[index][1]()            # selected by position
