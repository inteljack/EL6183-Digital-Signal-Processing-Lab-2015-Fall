#!/usr/local/bin/python
#####################################################################
# tools launcher; uses guimaker templates, guimixin std quit dialog;
# I am just a class library: run mytools script to display the gui;
#####################################################################

from Tkinter import *                               # get widgets
from PP2E.Gui.Tools.guimixin import GuiMixin        # get quit, notdone
from PP2E.Gui.Tools.guimaker import *               # menu/toolbar builder

class ShellGui(GuiMixin, GuiMakerWindowMenu):       # a frame + maker + mixins
    def start(self):                                # use GuiMaker if component
        self.setMenuBar()
        self.setToolBar()
        self.master.title("Shell Tools Listbox")
        self.master.iconname("Shell Tools")

    def handleList(self, event):                    # on listbox double-click
        label = self.listbox.get(ACTIVE)            # fetch selection text
        self.runCommand(label)                      # and call action here

    def makeWidgets(self):                          # add listbox in middle
        sbar = Scrollbar(self)                      # cross link sbar, list
        list = Listbox(self, bg='white')            # or use Tour.ScrolledList
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)                     # pack 1st=clip last
        list.pack(side=LEFT, expand=YES, fill=BOTH)       # list clipped first
        for (label, action) in self.fetchCommands():      # add to list-box
            list.insert(END, label)                       # and menu/toolbars
        list.bind('<Double-1>', self.handleList)          # set event handler
        self.listbox = list   

    def forToolBar(self, label):                          # put on toolbar?
        return 1                                          # default = all

    def setToolBar(self):
        self.toolBar = []
        for (label, action) in self.fetchCommands():
            if self.forToolBar(label):
                self.toolBar.append((label, action, {'side': LEFT}))
        self.toolBar.append(('Quit', self.quit, {'side': RIGHT}))

    def setMenuBar(self):
        toolEntries  = []
        self.menuBar = [ 
            ('File',  0, [('Quit', -1, self.quit)]),    # pull-down name
            ('Tools', 0, toolEntries)                   # menu items list
            ]                                           # label,underline,action
        for (label, action) in self.fetchCommands():
            toolEntries.append((label, -1, action))     # add app items to menu

###################################################
# delegate to template type-specific subclasses
# which delegate to app toolset-specific subclasses
###################################################

class ListMenuGui(ShellGui):
    def fetchCommands(self):             # subclass: set 'myMenu'
        return self.myMenu               # list of (label, callback)
    def runCommand(self, cmd):
        for (label, action) in self.myMenu: 
            if label == cmd: action()

class DictMenuGui(ShellGui):
    def fetchCommands(self):   return self.myMenu.items()
    def runCommand(self, cmd): self.myMenu[cmd]()
