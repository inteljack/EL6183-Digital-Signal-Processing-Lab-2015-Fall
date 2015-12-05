################################################################
# test the Python-coded COM server from Python two ways
################################################################

def testViaPython():                                 # test without com
    from comserver import MyServer                   # use Python class name
    object = MyServer()                              # works as for any class
    print object.Hello()
    print object.Square(8)
    print object.version

def testViaCom():
    from win32com.client import Dispatch             # test via client-side com
    server = Dispatch('PythonServers.MyServer')      # use Windows registry name
    print server.Hello()                             # call public methods
    print server.Square(12)
    print server.version                             # access attributes

if __name__ == '__main__':
    testViaPython()                                  # test module, server
    testViaCom()                                     # com object retains state
    testViaCom()
