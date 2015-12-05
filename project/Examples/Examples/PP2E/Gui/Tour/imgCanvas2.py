gifdir = "../gifs/"
from sys import argv
from Tkinter import *
filename = (len(argv) > 1 and argv[1]) or 'ora-lp.gif'    # name on cmdline?
win = Tk()
img = PhotoImage(file=gifdir+filename)
can = Canvas(win)
can.pack(fill=BOTH)
can.config(width=img.width(), height=img.height())        # size to img size
can.create_image(2, 2, image=img, anchor=NW)
win.mainloop()

