# hold on to your radio variables (an obscure thing, indeed)

from Tkinter import *      
root = Tk()                   

def radio1():                   # local vars are temporary
    #global tmp                 # making it global fixes the problem
    tmp = IntVar()
    for i in range(10): 
        rad = Radiobutton(root, text=str(i), value=i, variable=tmp)
        rad.pack(side=LEFT)
    tmp.set(5)    

radio1()
root.mainloop()
