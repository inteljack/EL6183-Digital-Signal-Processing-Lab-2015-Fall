from menu1 import Menu, ListMenu
import os, security, logger

class SecureMenu(Menu):
    def __init__(self):
        self.user = os.environ['USER']           # call 'Menu.__init__' here?...

    def run(self):
        for tool in self.menu.keys():            # add a pre-validation step
            if security.allow(tool, self.user):
                break
        else:
            print "You're not authorized for any menu selections"
            return
        Menu.run(self)
            
    def validate(self, tool, verbose=0):         # where do I get called?...
        if not security.allow(tool, self.user):  # what's 'tool' here?...
            if verbose: 
                print "unauthorized - try again"
            return 0
        return tool

    def input(self):
        option = Menu.input(self)                # where do I get called?...
        return self.validate(option, 1)          # add post-validation


class ListLogMenu(ListMenu):
    def __init__(self):
        self.user = os.environ['USER']           # 'ListMenu.__init__' here?...

    def runCommand(self, cmd):
        logger.record(self.user, cmd)            # add pre-logging
        ListMenu.runCommand(self, cmd)           # do normal list runCommand
