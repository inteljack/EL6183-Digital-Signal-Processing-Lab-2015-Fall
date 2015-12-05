#!/usr/local/bin/python

# the original, simpler but basic version from 
# the first edition; with packages and patches

from Tkinter  import *                                      # widgets, constants
from PP2E.Gui.Tools.guimixin import GuiMixin                # quit, help methods
from PP2E.Dbase.TableBrowser.guitools import frame, label, button, entry 

debugme = 1
def trace(*args):
    if debugme: print args


class CalcGui(GuiMixin, Frame):                        # the main class
    def __init__(self):                                # an extended frame
        Frame.__init__(self)                           # on default top-level
        self.pack(expand=YES, fill=BOTH)               # all parts expandable
        self.master.title('Python Calculator 0.2') 
        self.master.iconname("pcalc2")

        self.eval = Evaluator()                   # embed a stack handler
        self.text = StringVar()                   # make a linked variable
        self.text.set("0")
        self.erase = 1                            # clear "0" text next
        self.makeWidgets()                        # build the gui itself

    def makeWidgets(self):                        # 7 frames plus text-entry
        entry(self, TOP, self.text)
        rows = ["abcd", "0123", "4567", "89()"]
        for row in rows:
            frm = frame(self, TOP)
            for char in row: button(frm, LEFT, char, 
                               lambda x=self, y=char: x.onOperand(y))

        frm = frame(self, TOP)
        for char in "+-*/=": button(frm, LEFT, char,
                               lambda x=self, y=char: x.onOperator(y))

        frm = frame(self, TOP)
        button(frm, LEFT, 'cmd',  self.onMakeCommand) 
        button(frm, LEFT, 'dot',  lambda x=self: x.onOperand('.')) 
        button(frm, LEFT, 'help', self.help) 
        button(frm, LEFT, 'quit', self.quit)       # from guimixin

        frm = frame(self, BOTTOM)
        button(frm, LEFT, 'eval',  self.onEval)
        button(frm, LEFT, 'clear', self.onClear)

    def onClear(self):
        self.eval.clear()
        self.text.set('0')
        self.erase = 1

    def onEval(self): 
        self.eval.shiftOpnd(self.text.get())     # last or only opnd
        self.eval.closeall()                     # apply all optrs left
        self.text.set(self.eval.popOpnd())       # need to pop: optr next?
        self.erase = 1

    def onOperand(self, char):
        if char == '(':
            self.eval.open()
            self.text.set('(')                      # clear text next
            self.erase = 1
        elif char == ')':
            self.eval.shiftOpnd(self.text.get())    # last or only nested opnd
            self.eval.close()                       # pop here too: optr next?
            self.text.set(self.eval.popOpnd())
            self.erase = 1
        else:
            if self.erase:
                self.text.set(char)                     # clears last value
            else:
                self.text.set(self.text.get() + char)   # else append to opnd
            self.erase = 0

    def onOperator(self, char):
        self.eval.shiftOpnd(self.text.get())      # push opnd on left
        self.eval.shiftOptr(char)                 # eval exprs to left?
        self.text.set(self.eval.topOpnd())        # push optr, show opnd|result
        self.erase = 1                            # erased on next opnd|'('

    def onMakeCommand(self):                       
        new = Toplevel()                      # a new top-level window
        new.title('Enter Python command')     # arbitrary python code
        frm = frame(new, TOP)
        label(frm, LEFT, '>>>')
        ent = StringVar() 
        entry(frm, LEFT, ent)
        button(frm, RIGHT, 'Run', lambda s=self, e=ent: s.onCommand(e))

    def onCommand(self, entry):
        try:
            value = self.eval.runstring(entry.get())   
            entry.set('OKAY')  
            if value != None:                 # run in eval namespace dict
                self.text.set(value)          # expression or statement
                self.erase = 1             
        except:                               # result in calc field
            entry.set('ERROR')                # code in popup field


class Evaluator:
    def __init__(self):                         # expression evaluator
        self.names = {}                         # a names-space for vars
        self.opnd, self.optr = [], []           # two empty stacks
        self.runstring("from math import *")    # preimport math modules
        self.runstring("from random import *")  # into calc's namespace

    def clear(self):
        self.opnd, self.optr = [], []         # leave names intact

    def popOpnd(self):
        value = self.opnd[-1]                 # pop/return top|last opnd
        self.opnd[-1:] = []                   # to display and shift next
        return value 

    def topOpnd(self):
        return self.opnd[-1]                  # top operand (end of list)

    def open(self):
        self.optr.append('(')                 # treat '(' like an operator

    def close(self):                          # on ')' pop downto higest '('                     
        self.shiftOptr(')')                   # ok if empty: stays empty
        self.optr[-2:] = []                   # pop, or added again by optr
                                        
    def closeall(self):
        while self.optr:                      # force rest on 'eval'
            self.reduce()                     # last may be a var name
        try:                                 
            self.opnd[0] = self.runstring(self.opnd[0]) 
        except:
            self.opnd[0] = '*ERROR*'           # pop else added again next:
                                               # optrs assume next opnd erases
    def reduce(self):
        trace(self.optr, self.opnd) 
        try:                                   # collapse the top expr
            operator       = self.optr[-1]     # pop top optr (at end)
            [left, right]  = self.opnd[-2:]    # pop top 2 opnds (at end)
            self.optr[-1:] = []                # delete slice in-place
            self.opnd[-2:] = []
            result = self.runstring(left + operator + right)
            if result == None:
                result = left                   # assignment? key var name
            self.opnd.append(result)            # push result string back
        except:
            self.opnd.append('*ERROR*')         # stack/number/name error

    beatsMe = {'*': ['+', '-', '(', '='],       # class member
               '/': ['+', '-', '(', '='],       # optrs to not pop for key 
               '+': ['(', '='],                 # if prior optr is this: push
               '-': ['(', '='],                 # else: pop/eval prior optr
               ')': ['(', '='],                 # all left-associative as is
               '=': ['('] }

    def shiftOpnd(self, newopnd):               # push opnd at optr, ')', eval
        self.opnd.append(newopnd) 

    def shiftOptr(self, newoptr):               # apply ops with <= priority
        while (self.optr and
               not self.optr[-1] in self.beatsMe[newoptr]): 
            self.reduce()
        self.optr.append(newoptr)               # push this op above result

    def runstring(self, code):
        try:
            return `eval(code, self.names, self.names)`    # try expr: string
        except:
            exec code in self.names, self.names            # try stmt: None


if __name__ == '__main__': CalcGui().mainloop()
