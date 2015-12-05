# Note: can also start multiple copies of canvaspics.py 
# running in parallel, from operatin system: using '&' 
# in UNIX shell, double clicking on the file name more 
# than one in Windows explorer, and so on; as coded here,
# the windows receive user events independently, but 
# are part of the same process;

import sys
from Tkinter import *
from slideShow import SlideShow

if len(sys.argv) == 2:
    picdir = sys.argv[1]
else:
    picdir = '../gifs'

root = Tk()
Label(root, text="Two embedded slide shows: Toplevel windows").pack()
SlideShow(msecs=1000, parent=Toplevel(root), picdir=picdir).pack()
SlideShow(msecs=1000, parent=Toplevel(root), picdir=picdir).pack()
root.mainloop()
