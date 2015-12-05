# recode as an embeddable class

from Tkinter import *
from PP2E.Gui.Tour.quitter import Quitter          # reuse, pack, and grid

class SumGrid(Frame):
    def __init__(self, parent=None, numrow=5, numcol=5):
        Frame.__init__(self, parent)
        self.numrow = numrow                       # I am a frame container
        self.numcol = numcol                       # caller packs or grids me
        self.makeWidgets(numrow, numcol)           # else only usable one way

    def makeWidgets(self, numrow, numcol):
        self.rows = []
        for i in range(numrow):
            cols = []
            for j in range(numcol):
                e = Entry(self, relief=RIDGE)
                e.grid(row=i+1, column=j, sticky=NSEW)
                e.insert(END, '%d.%d' % (i, j))
                cols.append(e)
            self.rows.append(cols)

        self.sums = []
        for i in range(numcol):
            l = Label(self, text='?', relief=SUNKEN)
            l.grid(row=numrow+1, col=i, sticky=NSEW)
            self.sums.append(l)

        Button(self, text='Sum',   command=self.onSum).grid(row=0, column=0)
        Button(self, text='Print', command=self.onPrint).grid(row=0, column=1)
        Button(self, text='Clear', command=self.onClear).grid(row=0, column=2)
        Button(self, text='Load',  command=self.onLoad).grid(row=0, column=3)
        Quitter(self).grid(row=0, column=4)    # fails: Quitter(self).pack()

    def onPrint(self):
        for row in self.rows:
            for col in row:
                print col.get(),
            print
        print

    def onSum(self):
        t = [0] * self.numcol
        for i in range(self.numcol):
            for j in range(self.numrow):
                t[i]= t[i] + eval(self.rows[j][i].get())
        for i in range(self.numcol):
            self.sums[i].config(text=str(t[i]))

    def onClear(self):
        for row in self.rows:
            for col in row:
                col.delete('0', END)
                col.insert(END, '0.0')
        for sum in self.sums:
            sum.config(text='?')

    def onLoad(self):
        import string
        from tkFileDialog import *
        file = askopenfilename()
        if file:
            for r in self.rows:
                for c in r: c.grid_forget()
            for s in self.sums:
                s.grid_forget()
            filelines   = open(file, 'r').readlines()
            self.numrow = len(filelines)
            self.numcol = len(string.split(filelines[0]))
            self.makeWidgets(self.numrow, self.numcol)
            row = 0
            for line in filelines:
                fields = string.split(line)
                for col in range(self.numcol):
                    self.rows[row][col].delete('0', END)
                    self.rows[row][col].insert(END, fields[col])
                row = row+1

if __name__ == '__main__':
    import sys
    root = Tk()
    root.title('Summer Grid') 
    if len(sys.argv) != 3:
        SumGrid(root).pack()    # .grid() works here too
    else:
        rows, cols = eval(sys.argv[1]), eval(sys.argv[2])
        SumGrid(root, rows, cols).pack()
    mainloop()
