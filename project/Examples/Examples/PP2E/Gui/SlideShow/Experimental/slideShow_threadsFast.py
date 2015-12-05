# runs two slideshows as thread, changes 5 times/second
# you might be able to go a bit faster on your machine

import sys
from Tkinter import *
from slideShow_threads import SlideShow

if len(sys.argv) == 2:
    picdir = sys.argv[1]
else:
    picdir = '../gifs'

root = Tk()
Label(root, text="Two embedded slide shows: each side is a thread").pack()
SlideShow(root, msecs=200, picdir=picdir, bd=3, relief=SUNKEN).pack(side=LEFT)
SlideShow(root, msecs=200, picdir=picdir, bd=3, relief=SUNKEN).pack(side=LEFT)
root.mainloop()
