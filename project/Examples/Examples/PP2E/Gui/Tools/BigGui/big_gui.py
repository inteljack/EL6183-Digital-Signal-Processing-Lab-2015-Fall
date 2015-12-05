#!/usr/bin/python
#########################################################
# gui implementation - combines maker, mixin, and this
#########################################################

import sys, os, string
from Tkinter import *                        # widget classes
from PP2E.Gui.Tools.guimixin import *        # mix-in methods
from PP2E.Gui.Tools.guimaker import *        # frame, plus menu/toolbar builder
from find_demo_dir import findDemoDir        # Python demos search

class Hello(GuiMixin, GuiMakerWindowMenu):   # or GuiMakerFrameMenu
    def start(self):
        self.hellos = 0
        self.master.title("GuiMaker Demo")
        self.master.iconname("GuiMaker")

        self.menuBar = [                               # a tree: 3 pulldowns
          ('File', 0,                                  # (pull-down)
              [('New...',  0, self.notdone),           # [menu items list]
               ('Open...', 0, self.fileOpen), 
               ('Quit',    0, self.quit)]              # label,underline,action
          ),

          ('Edit', 0,
              [('Cut',  -1, self.notdone),             # no underline|action
               ('Paste',-1, self.notdone),             # lambda:0 works too 
               'separator',                            # add a separator
               ('Stuff', -1, 
                   [('Clone', -1, self.clone),         # cascaded submenu
                    ('More',  -1, self.more)] 
               ),
               ('Delete', -1, lambda:0),
               [5]]                                    # disable 'delete'
          ),

          ('Play', 0,
              [('Hello',     0, self.greeting),
               ('Popup...',  0, self.dialog),
               ('Demos', 0,
                  [('Hanoi', 0, 
                       lambda x=self: 
                        x.spawn(findDemoDir() + '\guido\hanoi.py', wait=0)),
                   ('Pong',  0, 
                       lambda x=self: 
                       x.spawn(findDemoDir() + '\matt\pong-demo-1.py', wait=0)),
                   ('Other...', -1, self.pickDemo)]
               )]
          )]

        self.toolBar = [
          ('Quit',  self.quit,     {'side': RIGHT}),        # add 3 buttons
          ('Hello', self.greeting, {'side': LEFT}),
          ('Popup', self.dialog,   {'side': LEFT, 'expand':YES}) ]

    def makeWidgets(self):                                  # override default
        middle = Label(self, text='Hello maker world!', width=40, height=10,
                       cursor='pencil', bg='white', relief=SUNKEN)
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos = self.hellos + 1
        if self.hellos % 3:
            print "hi"
        else:
            self.infobox("Three", 'HELLO!')    # on every third press

    def dialog(self):
        button = self.question('OOPS!', 
                               'You typed "rm*" ... continue?', 
                               'questhead', ('yes', 'no', 'help'))
        [lambda:0, self.quit, self.help][button]()

    def fileOpen(self):
        pick = self.selectOpenFile(file='big_gui.py')
        if pick:
            self.browser(pick)     # browse my source file, or other

    def more(self):
        new = Toplevel()
        Label(new,  text='A new non-modal window').pack()
        Button(new, text='Quit', command=self.quit).pack(side=LEFT)
        Button(new, text='More', command=self.more).pack(side=RIGHT)

    def pickDemo(self):
        pick = self.selectOpenFile(dir=findDemoDir()+'\guido')
        if pick:
            self.spawn(pick, wait=0)    # spawn any python program

if __name__ == '__main__':  Hello().mainloop()   # make one, run one
