# DEFUNCT
# use tuple assignment, not indexing
# not done: update for real tk8.0 menus???

##############################################################
# uses menu classes for layouts, instead of type tests
##############################################################

from Tkinter import *             # widget classes

#####################
# menu layout classes 
#####################

def addMenuItems(parent, items):
    menu = Menu(parent)
    for item in items:
        item.action(menu)
    return menu

class MenuCascade:
    def __init__(self, label, underline, cascade):
        self.label     = label
        self.underline = underline
        self.cascade   = cascade
    def action(self, menu):
        submenu = addMenuItems(menu, self.cascade) 
        menu.add_cascade(label     = self.label,      
                         underline = self.underline,   
                         menu      = submenu) 

class MenuItem:
    def __init__(self, label, underline, command):
        self.label     = label
        self.underline = underline
        self.command   = command
    def action(self, menu):
        menu.add_command(label     = self.label,
                         underline = self.underline,
                         command   = self.command)

class MenuSeparator:
    def action(self, menu):
        menu.add_separator({})

class MenuDisabler:
    def __init__(self, indexList):
        self.indexes = indexList
    def action(self, menu):
        for num in self.indexes:
            menu.entryconfig(num, state=DISABLED)


###########################
# customized guimaker class
###########################

import guimaker
class GuiMaker(guimaker.GuiMaker):
    def makeMenuBar(self):
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)
        for name, key, items in self.menuBar:
            mbutton = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            menu = addMenuItems(mbutton, items)
            mbutton['menu'] = menu
        if self.helpButton: 
            Button(menubar, text    = 'Help', 
                            cursor  = 'gumby', 
                            relief  = FLAT, 
                            command = self.help).pack(side=RIGHT)


##############################
# customized big_gui test code
##############################

if __name__ == '__main__': 
    from PP2E.Gui.WidgetTour.BigGui import big_gui2      # reuse test methods
    from guimixin import GuiMixin                        # get mix-in methods

    class Hello(GuiMixin, GuiMaker, big_gui2.Hello):     # use new GuiMaker
        def start(self):
            self.hellos = 1
            self.master.title("GuiMaker Demo - classes")
            self.master.iconname("GuiMaker")

            self.menuBar = [                            
              ('File', 0,                                
                  [MenuItem('New...',  0, self.notdone),   
                   MenuItem('Open...', 0, self.fileOpen),
                   MenuItem('Quit',    0, self.quit)]   
              ),

              ('Edit', 0,
                  [MenuItem('Cut',  -1, lambda:0),       
                   MenuItem('Paste',-1, lambda:0),
                   MenuSeparator(),              
                   MenuCascade('Stuff', -1,
                       [MenuItem('Clone', -1, self.clone),
                        MenuItem('More',  -1, self.more)]),
                   MenuItem('Delete', -1, lambda:0),
                   MenuDisabler([5])]                     
              ),

              ('Play', 0,
                  [MenuItem('Hello',     0, self.greeting),
                   MenuItem('Popup...',  0, self.dialog),
                   MenuCascade('Demos', 0,
                       [MenuItem('Hanoi', -1, self.notdone),
                        MenuItem('Pong',  -1, self.notdone),
                        MenuItem('Other...', -1, self.pickDemo)
                       ])
                  ]
              )]
            self.toolBar = [('Quit', self.quit, {})]

    Hello().mainloop()

