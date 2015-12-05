# must fetch before destroy with entries

from Tkinter import *
from entry2 import makeform, fetch, fields

def show(entries):
    fetch(entries)                  # must fetch before window destroyed!
    popup.destroy()                 # falls with msgs if stmt order is reversed

def ask():
    global popup
    popup = Toplevel()              # show form in modal dialog window
    ents = makeform(popup, fields)
    Button(popup, text='OK', command=(lambda e=ents: show(e)) ).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()             # wait for destroy here

root = Tk()
Button(root, text='Dialog', command=ask).pack()
root.mainloop()

