import time
for n in range(0,10):
	print n
	time.sleep(1)
	if n == 5:
		break

# from Tkinter import *

# class quitButton(Button):
#     def __init__(self, parent):
#         Button.__init__(self, parent)
#         self['text'] = 'Good Bye'
#         # Command to close the window (the destory method)
#         self['command'] = parent.destroy
#         self.pack(side=BOTTOM)

# root = Tk()
# quitButton(root)
# mainloop()

# # Run tkinter code in another thread

# from Tkinter import *
# import threading
# from flanger import *

# class App(threading.Thread):

# 	def __init__(self):
# 		threading.Thread.__init__(self)
# 		self.start()
	
# 	def Pressed(self):                          #function
# 		print self.v.get()

# 	def Parameter1(self,scaleValue):                          #function
# 		f = float(self.s1.get())
# 		w = 0.5
# 		print "Parameter1 is :", f
		
# 	def Parameter2(self,scaleValue):                          #function
# 		print "Parameter2 is :", float(self.s2.get())

# 	def Parameter3(self,scaleValue):                          #function
# 		print "Parameter3 is :", float(self.s3.get())

# 	def callback(self):
# 		self.root.quit()

# 	def run(self):
# 		self.root = Tk()
# 		self.root.protocol("WM_DELETE_WINDOW", self.callback)
# 		self.root.geometry("500x280+300+300")

# 		self.v = StringVar()
# 		self.v.set("Normal")
# 		self.s1 = DoubleVar()
# 		self.s1.set(0.0)
# 		self.s2 = DoubleVar()
# 		self.s2.set(0.0)
# 		self.s3 = DoubleVar()
# 		self.s3.set(0.0)

# 		label = Label(self.root, text="Hello World")
# 		label.pack(anchor=N, fill=X, expand=False)
# 		rad1 = Radiobutton(self.root, text='Flanger', value='Flanger', variable=self.v, command=self.Pressed)
# 		rad2 = Radiobutton(self.root, text='WahWah', value='WahWah', variable=self.v, command=self.Pressed)
# 		rad3 = Radiobutton(self.root, text='Normal', value='Normal', variable=self.v, command=self.Pressed)
# 		frame = Frame(self.root, relief = RAISED, borderwidth = 2)
# 		# frame.pack()
# 		scale1 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s1, command=self.Parameter1)
# 		scale2 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s2, command=self.Parameter2)
# 		scale3 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s3, command=self.Parameter3)

# 		scale1.pack(expand=True)
# 		scale2.pack(expand=True)
# 		scale3.pack(expand=True)
# 		frame.pack(side=LEFT, fill=BOTH, expand=True)
# 		rad1.pack(anchor=N, fill=X, expand=True)
# 		rad2.pack(anchor=N, fill=X, expand=True)
# 		rad3.pack(anchor=N, fill=X, expand=True)
# 		self.root.mainloop()


# app = App()
# print('Now we can continue running code while mainloop runs!')

# # flanger_effect(5,0.5)
# for i in range(100000):
#     print(i)

###################

# from Tkinter import *

# root = Tk()

# def task():
#     print("hello")
#     root.after(2000, task)  # reschedule event in 2 seconds

# root.after(2000, task)
# root.mainloop()


# #!/usr/bin/env python

# import matplotlib
# matplotlib.use('TkAgg')

# from numpy import arange, sin, pi
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# # implement the default mpl key bindings
# from matplotlib.backend_bases import key_press_handler


# from matplotlib.figure import Figure

# import sys
# if sys.version_info[0] < 3:
#     import Tkinter as Tk
# else:
#     import tkinter as Tk

# root = Tk.Tk()
# root.wm_title("Embedding in TK")


# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = arange(0.0, 3.0, 0.01)
# s = sin(2*pi*t)

# a.plot(t, s)


# # a tk.DrawingArea
# canvas = FigureCanvasTkAgg(f, master=root)
# canvas.show()
# canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

# toolbar = NavigationToolbar2TkAgg(canvas, root)
# toolbar.update()
# canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


# def on_key_event(event):
#     print('you pressed %s' % event.key)
#     key_press_handler(event, canvas, toolbar)

# canvas.mpl_connect('key_press_event', on_key_event)


# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# button = Tk.Button(master=root, text='Quit', command=_quit)
# button.pack(side=Tk.BOTTOM)

# Tk.mainloop()
# # If you put root.destroy() here, it will cause an error if
# # the window is closed with the window manager.


# import threading
# import time
# from flanger import *

# STATE = 0

# def worker(STATE):
#     # time.sleep(2)
# 	if STATE == 1:
# 		print threading.currentThread().getName(), 'Starting'
# 		flanger_effect(f,w)

# 	elif STATE == 0:
# 		print threading.currentThread().getName(), 'Exiting'

# def my_service(STATE):
#     print threading.currentThread().getName(), 'Starting'
#     time.sleep(3)
#     STATE = 1
#     print threading.currentThread().getName(), 'Exiting'

# t = threading.Thread(name='my_service', target=my_service(STATE))
# w = threading.Thread(name='worker', target=worker(STATE))
# w2 = threading.Thread(target=worker) # use default name

# t.start()
# w2.start()
# w.start()

# import Tkinter as tk

# def create_window():
#     window = tk.Toplevel(root)

# root = tk.Tk()
# b = tk.Button(root, text="Create new window", command=create_window)
# b.pack()

# root.mainloop()

# from Tkinter import *
# widget = Button(text='Spam', padx=10, pady=10)
# widget.pack(padx=100, pady=100)
# widget.config(cursor='gumby')
# widget.config(bd=8, relief=RAISED)
# widget.config(bg='dark green', fg='white')
# widget.config(font=('helvetica', 20, 'underline italic'))
# mainloop()

# import Tkinter as tk

# root = tk.Tk()
# tk.Label(root, text="this is the root window").pack()
# root.geometry("200x200")
# for i in range(4):
#     window = tk.Toplevel()
#     window.geometry("200x200")

#     tk.Label(window, text="this is window %s" % i).pack()

# root.mainloop()

