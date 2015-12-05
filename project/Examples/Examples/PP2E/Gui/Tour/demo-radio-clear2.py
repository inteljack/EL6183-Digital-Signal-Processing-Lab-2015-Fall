# hold on to your radio variables (an obscure thing, indeed)

from Tkinter import *      
root = Tk()                   

# this should come up with "5" selected initially, but doesn't
# local tmp is reclaimed, the Tk var is unset, and "5" setting is lost
# radio buttons work fine, though, one you start pressing (resets var)

def radio1(root):               # local vars are temporary
    #global tmp                 # making it global fixes the problem
    tmp = IntVar()
    for i in range(10): 
        rad = Radiobutton(root, text=str(i), value=i, variable=tmp)
        rad.pack(side=LEFT)
    tmp.set(5)    

# simulate a variable in an a data structure that is reclaimed
# here, the var is unset on an event, temporarily clearing the selection
# radio buttons work fine, though, one you start pressing (resets var)

def radio2(root):
    global var                  # a reference that goes away later 
    var  = IntVar() 
    for i in range(10):
        rad = Radiobutton(root, text=str(i), value=i, variable=var)
        rad.pack(side=LEFT)
    var.set(2)

def ondel():
    global var
    del var                     # or var.__del__() to trigger repeatedly

frm = Frame(); frm.pack(); radio1(frm)
frm = Frame(); frm.pack(); radio2(frm)
Button(root, text='del', command=ondel).pack()
root.mainloop()
