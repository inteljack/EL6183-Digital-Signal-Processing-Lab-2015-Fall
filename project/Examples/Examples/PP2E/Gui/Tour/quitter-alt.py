#############################################
# a quit button that verifies exit requests;
# to reuse, attach an instance to other guis
#############################################

from Tkinter import *                   # get widget classes
from tkMessageBox import askokcancel    # get canned dialog


class Quitter: 
    def __init__(self, parent=None):  
        self.widget = Button(parent, text='Quit', command=self.quit)
        self.widget.pack(side=LEFT)
    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: self.widget.quit()
    def __getattr__(self, name):
        return getattr(self.widget, name)

if __name__ == '__main__': Quitter().mainloop()

