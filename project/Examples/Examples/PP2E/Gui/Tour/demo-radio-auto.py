# radio buttons, the easy way

from Tkinter import *      
root = Tk()                     # IntVars work too
var  = IntVar()                 # state = var.get()
for i in range(10):
    rad = Radiobutton(root, text=str(i), value=i, variable=var)
    rad.pack(side=LEFT)
root.mainloop()
print var.get()                 # show state on exit
