# added extras for entry width, calcgui font/color

from Tkinter import *

def frame(root, side, **extras): 
    widget = Frame(root)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: apply(widget.config, (), extras)
    return widget

def label(root, side, text, **extras):
    widget = Label(root, text=text, relief=RIDGE) 
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: apply(widget.config, (), extras)
    return widget

def button(root, side, text, command, **extras): 
    widget = Button(root, text=text, command=command) 
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: apply(widget.config, (), extras)
    return widget

def entry(root, side, linkvar, **extras):
    widget = Entry(root, relief=SUNKEN, textvariable=linkvar)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras: apply(widget.config, (), extras)
    return widget
