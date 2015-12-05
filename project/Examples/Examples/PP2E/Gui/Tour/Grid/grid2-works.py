##################################################################
# works-- isolates grid box in a container of its own
##################################################################

from Tkinter import *
from grid2 import gridbox, packbox

root = Tk()
frm = Frame(root)
frm.pack()
gridbox(frm)      # must have its own parent in which to grid 
packbox(root)
Button(root, text='Quit', command=root.quit).pack()
mainloop()
