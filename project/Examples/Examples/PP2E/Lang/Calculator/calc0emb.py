from Tkinter  import *
from calc0 import CalcGui                       # add parent, no master calls

class Outer:
    def __init__(self, parent):                               # embed gui
        Label(parent, text='Calc Attachment').pack()          # side=top
        CalcGui(parent)                                       # add calc frame
        Button(parent, text='Quit', command=parent.quit).pack() 
        
root = Tk()
Outer(root)
root.mainloop()
