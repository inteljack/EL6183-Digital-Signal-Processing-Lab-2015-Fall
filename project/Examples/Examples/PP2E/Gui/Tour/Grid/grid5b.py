# add column sums, clearing

from Tkinter import *
numrow, numcol = 5, 4

rows = []
for i in range(numrow):
    cols = []
    for j in range(numcol):
        e = Entry(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END, '%d.%d' % (i, j))
        cols.append(e)
    rows.append(cols)

sums = []
for i in range(numcol):
    l = Label(text='?', relief=SUNKEN)
    l.grid(row=numrow, col=i, sticky=NSEW)
    sums.append(l)

def onPrint():
    for row in rows:
        for col in row:
            print col.get(),
        print
    print

def onSum():
    t = [0] * numcol
    for i in range(numcol):
        for j in range(numrow):
            t[i]= t[i] + eval(rows[j][i].get())
    for i in range(numcol):
        sums[i].config(text=str(t[i]))

def onClear():
    for row in rows:
        for col in row:
            col.delete('0', END)
            col.insert(END, '0.0')
    for sum in sums:
        sum.config(text='?')

import sys
Button(text='Sum',   command=onSum).grid(row=numrow+1, column=0)
Button(text='Print', command=onPrint).grid(row=numrow+1, column=1)
Button(text='Clear', command=onClear).grid(row=numrow+1, column=2)
Button(text='Quit',  command=sys.exit).grid(row=numrow+1, column=3)
mainloop()
