from Tkinter import *                # get base widget set
from dialogList import demos         # get dialog demo callbacks
from quitter import Quitter          # attach a quit frame object 

class PickDlgDemo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        Label(self,  text="Dialog picker demo - class").pack()
        Button(self, text="Run demo", command=self.pickDemo).pack(side=LEFT)
        Quitter(self).pack(side=RIGHT) 
        self.index = -1
    def pickDemo(self):
        self.index = (self.index + 1) % len(demos)
        print demos[self.index]()

PickDlgDemo().mainloop()
