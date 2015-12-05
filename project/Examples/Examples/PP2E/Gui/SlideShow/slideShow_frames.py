import sys
from Tkinter import *
from slideShow import SlideShow

if len(sys.argv) == 2:
    picdir = sys.argv[1]
else:
    picdir = '../gifs'

root = Tk()
Label(root, text="Two embedded slide shows: Frames").pack()
SlideShow(parent=root, picdir=picdir, bd=3, relief=SUNKEN).pack(side=LEFT)
SlideShow(parent=root, picdir=picdir, bd=3, relief=SUNKEN).pack(side=RIGHT)
root.mainloop()
