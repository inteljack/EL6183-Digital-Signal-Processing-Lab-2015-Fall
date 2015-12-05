from Tkinter import *                   # get widget classes
root = Tk()
widget = Button(root, text='Hello world', command=root.quit)
widget.pack()
root.mainloop()
