# see what happens when some buttons have same value

from Tkinter import *      
root = Tk()
var = StringVar()
for i in range(10):
    rad = Radiobutton(root, text=str(i), variable=var, value=str(i % 3))
    rad.pack(side=LEFT)
root.mainloop()
