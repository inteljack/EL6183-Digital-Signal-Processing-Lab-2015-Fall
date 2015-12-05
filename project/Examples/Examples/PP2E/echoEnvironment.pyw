# Displays important environment settings in pop-up windows
import sys, os, string

def showinfo(label, message, useMessageBox=0):
    if useMessageBox:                                    # use canned popup?
        import tkMessageBox                              # on Linux, this shows
        tkMessageBox.showinfo(label, message)            # long messages poorly
    else:
        from Tkinter import *
        from ScrolledText import ScrolledText            # roll our own popup
        new = Toplevel()                                 # make a new window
        new.title(label)
        new.bind("<Return>", (lambda event, new=new: new.destroy()))
        ok = Button(new, text="OK", command=new.destroy)
        ok.pack(pady=1, side=BOTTOM)                     # pack first=clip last
        text = ScrolledText(new, bg='beige')             # add Text + scrollbar
        text.insert('0.0', message)
        text.pack(expand=YES, fill=BOTH)
        ok.focus_set()                      # make new window modal:
        new.grab_set()                      # get keyboard focus, grab app
        new.wait_window()                   # don't return till new.destroy

def formatlist(list, rawform):
    return ('[\n' + string.join(list, ',\n') + '\n]' + 
            '\n\nRAW=>\n' + rawform)

def splitpath(pathstring):
    pathlist = string.split(pathstring, os.pathsep)
    return formatlist(pathlist, pathstring)

if __name__ == '__main__':
    useMBox = (len(sys.argv) > 1)           # true only if a command-line arg 
    from Tkinter import Label
    Label(text='\n\tEnvironment setttings\t\n', bg='white').pack()

    for var in ('PYTHONPATH', 'PATH', 'PP2E_PYTHON_FILE', 'PP2E_EXAMPLE_DIR'):
        try:
            showinfo('os.environ["%s"]' % var, 
                      splitpath(os.environ[var]), useMBox)
        except: 
            showinfo('os.environ["%s"]' % var, '(%s is not set)' % var, useMBox)

    showinfo('sys.path', formatlist(sys.path, str(sys.path)), useMBox)
