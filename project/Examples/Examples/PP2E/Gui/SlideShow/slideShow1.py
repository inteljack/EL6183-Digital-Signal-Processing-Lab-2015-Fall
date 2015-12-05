from Tkinter import *
from glob import glob
from tkMessageBox import askyesno
from tkFileDialog import askopenfilename
import random

def makeWidgets(root):
    global mycanvas, myonoff
    mycanvas = Canvas(root, bg='white')
    mycanvas.pack(side=LEFT, expand=YES, fill=BOTH)
    myonoff = Button(root, text='Start', command=onStart)
    myonoff.pack(fill=BOTH)
    Button(root, text='Open',  command=onOpen).pack(fill=BOTH)
    Button(root, text='Beep',  command=onBeep).pack(fill=BOTH)
    Button(root, text='Quit',  command=onQuit).pack(fill=BOTH)

def onStart():
    global myloop
    myloop = 1
    myonoff.config(text='Stop', command=onStop)
    onTimer()

def onStop():
    global myloop
    myloop = 0
    myonoff.config(text='Start', command=onStart)

def onOpen():
    global myimage
    onStop()
    pick = askopenfilename(initialdir=myopens)
    if pick:
        myimage = PhotoImage(file=pick)
        mycanvas.config(height=myimage.height(), width=myimage.width())
        mycanvas.create_image(2, 2, image=myimage, anchor=NW)

def onQuit():
    if askyesno('Verify', 'Really quit?'):
        root.quit()

def onBeep():
    global mybeep
    mybeep = mybeep ^ 1

def onTimer():
    global myimage
    if myloop:
        pick = random.choice(myfiles)
        myimage = PhotoImage(file=pick)
        mycanvas.create_image(2, 2, image=myimage, anchor=NW)
        if mybeep: root.bell()
        root.after(mymsecs, onTimer)    # reschedule

import sys
if len(sys.argv) == 2:
    myopens = sys.argv[1]                      # if arg, it's the image dir
else:
    myopens = '../gifs'                        # else default to startdir/gifs
myfiles = glob(myopens + '/*.gif')             # only show gifs (for now)

root = Tk()
makeWidgets(root)
mymsecs = 2000
mybeep  = 1
root.mainloop()

