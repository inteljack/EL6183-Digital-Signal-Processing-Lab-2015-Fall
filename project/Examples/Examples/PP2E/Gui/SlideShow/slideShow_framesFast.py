import sys
from Tkinter import *
from slideShow import SlideShow

if len(sys.argv) == 2:
    picdir = sys.argv[1]
else:
    picdir = '../gifs'

root = Tk()
Label(root, text="Two embedded slide shows: each side uses after() loop").pack()
SlideShow(msecs=200, 
          parent=root, picdir=picdir, bd=3, relief=SUNKEN).pack(side=LEFT)
SlideShow(msecs=200, 
          parent=root, picdir=picdir, bd=3, relief=SUNKEN).pack(side=RIGHT)
root.mainloop()
