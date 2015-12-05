DEFUNCT -- big-gui wihout guimaker...

#!/usr/local/bin/python
from Tkinter  import *                                # widget classes
from PP2E.Gui.Tools.guimixin import GuiMixin          # mix-in methods

class Hello(GuiMixin, Frame):
    def __init__(self, master=None):
	Frame.__init__(self, master)
	Pack.config(self)
	self.createWidgets()
        self.hellos = 1
        self.master.title("Buttons, Menus, and More")
        self.master.iconname("tkpython")

    def createWidgets(self):
        self.makeMenuBar()
        Label(self, {'text':   'Hello GUI world!', 
                     'cursor': 'pencil',
                      Pack:    {'padx': 50, 'pady':50} })
        self.makeToolBar()

    def makeMenuBar(self):
        self.menubar = Frame(self, {'relief': 'raised', 'bd': 2, 
                                     Pack: {'side': 'top', 'fill': 'x'}})
        pulldowns = self.fileMenu(), self.editMenu(), self.playMenu()
        apply(self.menubar.tk_menuBar, pulldowns)
        Button(self.menubar,
              {'text':   'Help', 
               'cursor': 'gumby',
               'relief': 'flat',
               'command': self.help,
                Pack: {'side': 'right', 'padx': '1m'}})

    def makeToolBar(self):
        self.toolbar = Frame(self, {'cursor': 'hand2',
                                    'relief': 'sunken', 'bd': 2, 
                                     Pack: {'side': 'bottom', 'fill': 'x'} })
	Button(self.toolbar, 
               {'text':   'Quit', 
                'command': self.quit, Pack:{'side': 'right'} })
	Button(self.toolbar, 
               {'text':   'Hello', 
                'command': self.greeting, Pack:{'side': 'left'} })
	Button(self.toolbar, 
               {'text':   'Popup', 
                'command': self.dialog, Pack:{'side': 'left', 'expand':1 } })

    def fileMenu(self):
        mbutton = Menubutton(self.menubar,
                                   {'text': 'File', 
                                    'underline': 0,
                                     Pack: {'side': 'left', 'padx': '1m'}})
        menu = Menu(mbutton)
        menu.add('command', {'label':    'New...', 
                             'underline': 0, 
                             'command':   self.notdone})
        menu.add('command', {'label':    'Open...', 	
                             'underline': 0,
                             'command':   self.fileOpen})
        menu.add('command', {'label':    'Quit', 
                             'underline': 0,
                             'command':   self.quit})
        mbutton['menu'] = menu
        return mbutton

    def editMenu(self):
        mbutton = Menubutton(self.menubar, 
                                   {'text': 'Edit', 
                                    'underline': 0,
                                     Pack: {'side': 'left', 'padx': '1m'}})
        menu = Menu(mbutton)
        menu.add_command({'label': 'Cut'})
        menu.add_command({'label': 'Paste'})
        menu.add_separator({})

        submenu = Menu(mbutton) 
        submenu.add_command({'label': 'Clone', 'command': self.clone})
        submenu.add_command({'label': 'More',  'command': self.more})
        menu.add_cascade({'label': 'Stuff', 'menu': submenu})
                          
        menu.add_command({'label': 'Delete'})
        menu.entryconfig(5, {"state" : "disabled"})
        mbutton['menu'] = menu
        return mbutton

    def playMenu(self):
        mbutton = Menubutton(self.menubar, 
                                   {'text': 'Play',
	                            'underline': 0,
                                     Pack: {'side': 'left', 'padx': '1m'}})
        menu = Menu(mbutton)
        menu.add_command({'label':  'Hello',    'underline': 0,
                          'command': self.greeting})
        menu.add_command({'label':  'Popup...', 'underline': 0,
                          'command': self.dialog})

        submenu = Menu(mbutton) 
        submenu.add_command({'label': 'Hanoi', 
                             'command': 
                              lambda x=self: x.spawn('guido/hanoi.py', 1) }) 
        submenu.add_command({'label': 'Pong',  
                             'command': 
                              lambda x=self: x.spawn('matt/pong-demo-1.py') })
        menu.add_cascade({'label': 'Demos', 'menu': submenu, 'underline': 0})

        mbutton['menu'] = menu
        return mbutton

    def greeting(self):
        self.hellos = self.hellos + 1
        if self.hellos % 3:
            print "hi"
        else:
            self.infobox("Gotcha'", 'HELLO!')

    def dialog(self):
        button = self.question('OOPS!', 'You typed "rm*" ... continue?', 
                               'questhead', ('yes', 'no', 'help'))
        [lambda:0, self.quit, self.help][button]()

    def fileOpen(self):
        self.browser('big_gui-0.py')       # browse self; hmm...

    def more(self):
        new = Toplevel()
        new.label = Label(new, {'text': 'A new non-modal window'})
        new.label.pack()
        Button(new, {'text':'Quit', 'command':self.quit, Pack:{'side':'left'}})
        Button(new, {'text':'More', 'command':self.more, Pack:{'side':'right'}})

if __name__ == '__main__':  Hello().mainloop()




# use: 'big_gui1.py', 'python big_gui1.py' 
# demo's, menus, buttons, dialogs, text, forks,..

# note: lambda: self=x...
# note [...][button]()
# note: multi-inher-- GuiMixin before Frame in class header! 
# note: not expandable: inherited from GuiMaker in big_gui2
# else self.quit from Frame and exits silently...

