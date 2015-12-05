from Tkinter import *
import sys
exec 'from %s import Demo' % sys.argv[1]         # import by name string
root = Tk()
demo = Demo(root)
Button(Toplevel(), text='state', command=demo.report).pack(fill=X)
root.mainloop()
