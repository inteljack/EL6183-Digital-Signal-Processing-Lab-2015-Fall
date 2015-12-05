from Tkinter import *
from flanger import *
# from ttk import *

#####Color table#####
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)

def Pressed():                          #function
        print v.get()

def Parameter1(scaleValue):                          #function
        f = float(s1.get())
        w = 0.5
        print "Parameter1 is :", float(s1.get())
        flanger_effect(f,w)

def Parameter2(scaleValue):                          #function
        print "Parameter2 is :", float(s2.get())

def Parameter3(scaleValue):                          #function
        print "Parameter3 is :", float(s3.get())

def Call():
        lab= Label(root, text = 'You pressed\nthe button')
        lab.pack()
        button['bg'] = 'blue'
        button['fg'] = 'white'
# class Radiobar(Frame):
#     def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
#         Frame.__init__(self, parent)
#         self.var = StringVar()
#         for pick in picks:
#             rad = Radiobutton(self, text=pick, value=pick, variable=self.var, command=pressed)
#             rad.pack(side=side, anchor=anchor, expand=YES)
#     def state(self):
#         return self.var.get()

root = Tk()                             #main window
root.geometry("500x280+300+300")
# root.geometry('100x110+350+70')
v = StringVar()
v.set("Normal")
s1 = DoubleVar()
s1.set(0.0)
s2 = DoubleVar()
s2.set(0.0)
s3 = DoubleVar()
s3.set(0.0)
print v.get()
rad1= Radiobutton(root, text='Flanger', value='Flanger', variable=v, command=Pressed)
rad2 = Radiobutton(root, text='WahWah', value='WahWah', variable=v, command=Pressed)
rad3 = Radiobutton(root, text='Normal', value='Normal', variable=v, command=Pressed)
frame = Frame(root, relief = RAISED, borderwidth = 2)
scale1 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=s1, command=Parameter1)
scale2 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=s2, command=Parameter2)
scale3 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=s3, command=Parameter3)

scale1.pack(expand=True)
scale2.pack(expand=True)
scale3.pack(expand=True)
# scrollbar1 = Scrollbar(frame, orient=HORIZONTAL)
# scrollbar2 = Scrollbar(frame, orient=HORIZONTAL)
# scrollbar3 = Scrollbar(frame, orient=HORIZONTAL)

frame.pack(side=LEFT, fill=BOTH, expand=True)
# scrollbar1.pack(side=TOP, fill=X, expand=True)
# scrollbar2.pack(side=TOP, fill=X, expand=True)
# scrollbar3.pack(side=TOP, fill=X, expand=True)

rad1.pack(anchor=N, fill=X, expand=True)
rad2.pack(anchor=N, fill=X, expand=True)
rad3.pack(anchor=N, fill=X, expand=True)
# rad.config(relief=RIDGE, bd=2)

# gui = Radiobar(root, ['flanger', 'WahWah', 'Normal'], side=TOP, anchor=NW)
# gui.pack(side=RIGHT, fill=Y)
# gui.config(relief=RIDGE,  bd=2)

# button1 = Button(root, text = 'Press', command = Pressed)
# button1.pack(side = RIGHT, pady = 5, padx = 5)
# button2 = Button(root, text = 'Press', command = Pressed)
# button2.pack(side = RIGHT, pady = 5, padx = 5)

# button = Button(root, text = 'Press me', command = Call)
# button.pack()
# Pressed()


root.mainloop()

