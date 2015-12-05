from Tkinter import *
from calc0 import CalcGui

class Inner(CalcGui):                                          # extend gui
    def __init__(self):
        CalcGui.__init__(self)
        Label(self,  text='Calc Subclass').pack()              # add after
        Button(self, text='Quit', command=self.quit).pack()    # top implied
        
Inner().mainloop()
