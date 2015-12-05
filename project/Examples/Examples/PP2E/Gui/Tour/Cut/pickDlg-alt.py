from Tkinter import *                # get base widget set
from dialogList import demos         # get dialog demo callbacks
from quitter import Quitter          # attach a quit object to me

class PickDlgDemo:
    def __init__(self, parent=None):
        win = Frame(parent)
        win.pack()
        Label(win,  text="Dialog picker demo - alt class").pack()
        Button(win, text="Run demo", command=self.pickDemo).pack(side=LEFT)
        Quitter(win).pack(side=RIGHT) 
        self.index = -1
    def pickDemo(self):
        self.index = (self.index + 1) % len(demos)
        print demos[self.index]()

PickDlgDemo()
mainloop()         # from Tknter, not in pickDlgDemo

