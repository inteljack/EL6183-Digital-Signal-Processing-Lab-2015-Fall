# a reusable form class, used by getfilegui (and others)

from Tkinter import *
entrysize = 40

class Form:                                           # add non-modal form box
    def __init__(self, labels, parent=None):          # pass field labels list
        box = Frame(parent)
        box.pack(expand=YES, fill=X)
        rows = Frame(box, bd=2, relief=GROOVE)        # box has rows, button
        lcol = Frame(rows)                            # rows has lcol, rcol
        rcol = Frame(rows)                            # button or return key,
        rows.pack(side=TOP, expand=Y, fill=X)         # runs onSubmit method
        lcol.pack(side=LEFT)
        rcol.pack(side=RIGHT, expand=Y, fill=X)
        self.content = {}
        for label in labels:
            Label(lcol, text=label).pack(side=TOP)
            entry = Entry(rcol, width=entrysize)
            entry.pack(side=TOP, expand=YES, fill=X)
            self.content[label] = entry
        Button(box, text='Cancel', command=self.onCancel).pack(side=RIGHT)
        Button(box, text='Submit', command=self.onSubmit).pack(side=RIGHT)
        box.master.bind('<Return>', (lambda event, self=self: self.onSubmit()))

    def onSubmit(self):                                      # override this
        for key in self.content.keys():                      # user inputs in 
            print key, '\t=>\t', self.content[key].get()     # self.content[k]

    def onCancel(self):                                      # override if need
        Tk().quit()                                          # default is exit

class DynamicForm(Form):
    def __init__(self, labels=None):
        import string
        labels = string.split(raw_input('Enter field names: '))
        Form.__init__(self, labels)
    def onSubmit(self):
        print 'Field values...'
        Form.onSubmit(self)           
        self.onCancel()              
        
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        Form(['Name', 'Age', 'Job'])     # precoded fields, stay after submit
    else:
        DynamicForm()                    # input fields, go away after submit
    mainloop()    
