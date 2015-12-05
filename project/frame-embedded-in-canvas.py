from Tkinter import *

def yscroll(*args):
    # print('yscroll: {}'.format(args))
    scrollbar.set(*args)

def yview(*args):
    print('view: {}'.format(args))
    textbox.yview(*args)

root = Tk()    
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)    
textbox = Text(root, yscrollcommand=yscroll)
for i in range(100):
    textbox.insert(END, '{}\n'.format(i))
textbox.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=yview)
mainloop()