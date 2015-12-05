####################################################
# same, but show returns values of dialog calls;
# the lambda saves data from the local scope to be 
# passed to the handler (button handlers normally 
# get no args) and works like this def statement:
# def func(self=self, name=key): self.printit(name)
####################################################

from Tkinter import *              # get base widget set
from dialogTable import demos      # button callback handlers
from quitter import Quitter        # attach a quit object to me

class Demo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        Label(self, text="Basic demos").pack()
        for (key, value) in demos.items():
            func = (lambda self=self, name=key: self.printit(name))      
            Button(self, text=key, command=func).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)
    def printit(self, name): 
        print name, 'returns =>', demos[name]()      # fetch, call, print

if __name__ == '__main__': Demo().mainloop()
