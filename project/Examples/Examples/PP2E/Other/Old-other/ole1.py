# Expose the Python interpreter to OLE.
# Called whenever an OLE object called 
# "Python.Interpreter" is invoked.

class OLEInterpreter(OleDocServer):
    def __init__(self):
        dispids={1: ("Eval", self.Eval), 2: ("Exec", self.Exec)}
        OleDocServer.__init__(self, 
              "{30BD3490-2632-11cf-AD5B-524153480001}", dispids)

    def Eval(self, exp):
        if type(exp)<>type(''):
            raise oleautsv.exc_type_mismatch, (1, "Argument must be a string")
        return eval(exp)

    def Exec(self, exp):
        if type(exp)<>type(''):
            raise oleautsv.exc_type_mismatch, (1, "Argument must be a string")
        exec exp
