################################################################
# a COM server coded in Python; the _reg_ class attributes 
# give registry parameters, and others list methods and attrs;
# for this to work, you must install Python and the win32all 
# package, this module file must live on your Python path,
# and the server must be registered to COM (see code at end);
# run pythoncom.CreateGuid() to make your own _reg_clsid_ key;
################################################################

import sys
from   win32com.server.exception import COMException         # what to raise 
import win32com.server.util                                  # server tools
globhellos = 0

class MyServer:

    # com info settings
    _reg_clsid_      = '{1BA63CC0-7CF8-11D4-98D8-BB74DD3DDE3C}'
    _reg_desc_       = 'Example Python Server'
    _reg_progid_     = 'PythonServers.MyServer'              # external name
    _reg_class_spec_ = 'comserver.MyServer'                  # internal name
    _public_methods_ = ['Hello', 'Square']
    _public_attrs_   = ['version']

    # python methods
    def __init__(self):  
        self.version = 1.0
        self.hellos  = 0
    def Square(self, arg):                                   # exported methods
        return arg ** 2
    def Hello(self):                                         # global variables
        global globhellos                                    # retain state, but
        globhellos  = globhellos  + 1                        # self vars don't
        self.hellos = self.hellos + 1
        return 'Hello COM server world [%d, %d]' % (globhellos, self.hellos)

# registration functions
def Register(pyclass=MyServer):
    from win32com.server.register import UseCommandLine
    UseCommandLine(pyclass)
def Unregister(classid=MyServer._reg_clsid_):
    from win32com.server.register import UnregisterServer
    UnregisterServer(classid)

if __name__ == '__main__':       # register server if file run or clicked
    Register()                   # unregisters if --unregister cmd-line arg
