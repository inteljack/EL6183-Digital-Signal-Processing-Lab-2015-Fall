########################################################################
# a container with an extra row of buttons for common operations;
# a more useful customization: adds buttons for more operations (sqrt,
# 1/x, etc.) by embedding/composition, not subclassing; new buttons are
# added after entire CalGui frame because of the packing order/options;
########################################################################

from Tkinter import *
from calculator import CalcGui, getCalcArgs
from PP2E.Dbase.TableBrowser.guitools import frame, button, label

class CalcGuiPlus(Toplevel): 
    def __init__(self, **args):
        Toplevel.__init__(self)
        label(self, TOP, 'PyCalc Plus - Container')
        self.calc = apply(CalcGui, (self,), args)
        frm = frame(self, BOTTOM)
        extras = [('sqrt', 'sqrt(%s)'),
                  ('x^2 ',  '(%s)**2'),  
                  ('x^3 ',  '(%s)**3'),
                  ('1/x ',  '1.0/(%s)')]
        for (lab, expr) in extras:
            button(frm, LEFT, lab, (lambda m=self.onExtra, e=expr: m(e)) )
        button(frm, LEFT, ' pi ', self.onPi)
    def onExtra(self, expr):
        text = self.calc.text
        eval = self.calc.eval
        try:
            text.set(eval.runstring(expr % text.get()))
        except:
            text.set('ERROR')
    def onPi(self):
        self.calc.text.set(self.calc.eval.runstring('pi'))

if __name__ == '__main__': 
    root = Tk()
    button(root, TOP, 'Quit', root.quit)
    apply(CalcGuiPlus, (), getCalcArgs()).mainloop()     # -bg,-fg to calcgui
