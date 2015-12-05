#!/usr/local/bin/python
######################################################
# pack text files into one, separated by marker line;
# % packapp.py -v -o target src src...
# % packapp.py *.txt -o packed1
# >>> apptools.appRun('packapp.py', args...)
# >>> apptools.appCall(PackApp, args...)
######################################################

from textpack import marker
from PP2E.System.App.Kinds.redirect import StreamApp

class PackApp(StreamApp):
    def start(self):
        StreamApp.start(self)
        if not self.args:
            self.exit('packapp.py [-o target]? src src...')
    def run(self):
        for name in self.restargs():
            try:
                self.message('packing: ' + name)
                self.pack_file(name)
            except:
                self.exit('error processing: ' + name)
    def pack_file(self, name):  
        self.setInput(name)             
        self.write(marker + name + '\n')
        while 1:
            line = self.readline()
            if not line: break
            self.write(line)

if __name__ == '__main__':  PackApp().main()
