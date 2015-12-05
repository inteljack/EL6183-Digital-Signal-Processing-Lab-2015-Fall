#!/usr/local/bin/python 
# Older style frame-based menus

from Tkinter import *                              # get widget classes
from tkMessageBox import *                         # get common dialogs

class OldMenuDemo(Frame):                          # an extended frame
    def __init__(self, parent=None):               # attach to top-level?
        Frame.__init__(self, parent)               # do superclass init
        self.pack()
        self.createWidgets()                       # attach frames/widgets
        self.master.title("Buttons and Menus")     # set window-manager info
        self.master.iconname("tkpython")           # label when iconified

    def createWidgets(self):
        self.makeMenuBar()
        Label(self, text='Hello menu/toolbar world').pack(padx=30, pady=30)
        self.makeToolBar()

    def makeToolBar(self):
        toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
        toolbar.pack(side=BOTTOM, fill=X)
        Button(toolbar, text='Quit',  command=self.quit    ).pack(side=RIGHT)
        Button(toolbar, text='Hello', command=self.greeting).pack(side=LEFT)

    def makeMenuBar(self):
        self.menubar = Frame(self, relief=RAISED, bd=2)
        self.menubar.pack(side=TOP, fill=X)
        self.fileMenu()
        self.editMenu()

    def fileMenu(self):
        mbutton = Menubutton(self.menubar, text='File', underline=0)
        mbutton.pack(side=LEFT)
        menu = Menu(mbutton)
        menu.add_command(label='New...',  command=self.notdone)
        menu.add_command(label='Open...', command=self.notdone)
        menu.add_command(label='Quit',    command=self.quit)
        mbutton['menu'] = menu
        return mbutton

    def editMenu(self):
        mbutton = Menubutton(self.menubar, text='Edit', underline=0)
        mbutton.pack(side=LEFT)
        menu = Menu(mbutton)
        menu.add_command(label='Cut',   command=self.notdone)
        menu.add_command(label='Paste', command=self.notdone)
        menu.add_separator({})

        submenu = Menu(menu)
        submenu.add_command(label='Spam', command=self.notdone)
        submenu.add_command(label='Eggs', command=self.greeting)
        menu.add_cascade(label='Stuff', menu=submenu)

        menu.add_command(label='Delete', command=self.greeting)
        menu.entryconfig(2, state=DISABLED)
        mbutton['menu'] = menu
        return mbutton

    def greeting(self):
        showinfo('greeting', 'Greetings')
    def notdone(self):
        showerror('Not implemented', 'Not yet available')
    def quit(self):
        if askyesno('Verify quit', 'Are you sure you want to quit?'):
            Frame.quit(self)

if __name__ == '__main__':  OldMenuDemo().mainloop()  # if I'm run as a script
