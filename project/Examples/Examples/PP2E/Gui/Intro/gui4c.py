# creation order irrelevant to clipping

from Tkinter import *

def greeting():
    print 'Hello stdout world!...'

win = Frame()	
win.pack()

B1 = Button(win, text='Hello', command=greeting)
B2 = Button(win, text='Quit',  command=win.quit)
LB = Label(win,  text='Hello container world')

B1.pack(side=BOTTOM) #LEFT)
B2.pack(side=RIGHT)
LB.pack(side=TOP)


win.mainloop()
