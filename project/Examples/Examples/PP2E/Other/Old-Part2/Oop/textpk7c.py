#!/usr/local/bin/python

from interact import ListMenu               # get menu interaction
import textpak8                             # get pack/unpack methods

class TextPak(ListMenu, textpak8.TextPak):        # Menu's evalCommand,...
    def __init__(self):                           # textpak8's pack/unpack
        self.prompt = '>'
        self.menu = [ ('pack',   self.pack),      # call inherited methods
                      ('unpack', self.unpack),    # not textpak2 functions
                      ('stop',   self.stop) ] 

    def stop(self): return 1

if __name__ == '__main__': TextPak().run()
