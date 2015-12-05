from Tkinter import *            # get base widget set
from dialogList import demos     # get dialog demo callbacks
from quitter import Quitter      # attach a quit object to me

def pickDemo():
    global index
    index = (index + 1) % len(demos)
    print demos[index]()

root = Tk()
Label(root,  text="Dialog picker demo - basic").pack()
Button(root, text="Run demo", command=pickDemo).pack(side=LEFT)
Quitter(root).pack(side=RIGHT) 
index = -1
root.mainloop()
