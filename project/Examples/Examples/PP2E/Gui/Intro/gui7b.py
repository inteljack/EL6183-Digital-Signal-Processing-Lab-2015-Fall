from Tkinter import *
from gui7 import HelloPackage      # or get from gui7c--__getattr__ added

frm = Frame()
frm.pack()
Label(frm, text='hello').pack()

part = HelloPackage(frm)
part.pack(side=RIGHT)              # fails!--need part.top.pack(side=RIGHT) 
frm.mainloop()
