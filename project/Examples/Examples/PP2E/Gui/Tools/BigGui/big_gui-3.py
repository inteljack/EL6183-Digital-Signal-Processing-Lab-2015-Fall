#!/usr/local/bin/python

from Tkinter  import *                         # widget classes
import big_gui                                 # reuse callback handler methods
from PP2E.Gui.Tools.guimixin import GuiMixin   # mix-in methods
from PP2E.Gui.Tools.guimaker import GuiMaker   # frame, menu/toolbar builder

class Hello(GuiMixin, GuiMaker, big_gui.Hello):
    def start(self):
        self.hellos = 1
        self.master.title("GuiMaker Demo")
        self.master.iconname("GuiMaker")

        self.menuBar = [                               # a tree: 3 pulldowns
          ('File', 0,                                  # (pull-down)
              [('New...',  0, self.notdone),           # [menu items list]
               ('Open...', 0, self.fileOpen), 
               ('Quit',    0, self.quit)]              # label,underline,action
          ),

          ('Edit', 0,
              [('Cut',  -1, lambda:0),                 # no underline|action
               ('Paste',-1, lambda:0), 
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
                  [('Hanoi', -1, self.notdone),
                   ('Pong',  -1, self.notdone)]
               )]
          )]

        self.toolBar = [
	  ('Quit',  self.quit,     {'side': 'right'}),      # add 3 buttons
	  ('Hello', self.greeting, {'side': 'left'}),
          ('Popup', self.dialog,   {'side': 'left', 'expand':1 }) ]

    def makeWidgets(self):                                  # override default
        Label(self, {'text':   'Hello maker world!',        # add middle part
                     'cursor': 'pencil',
                      Pack: {'padx':50,'pady':50,'expand':'yes','fill':'both'}})

    def fileOpen(self): self.browser('big_gui-3.py') 

if __name__ == '__main__':  Hello().mainloop()   
