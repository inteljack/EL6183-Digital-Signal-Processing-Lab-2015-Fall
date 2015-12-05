#!/usr/local/bin/python
# file tools2.py: collected shell-tool menu
# todo: general expected-args format scheme
# todo: add a submenu for the last few items


import string
from PP2E.System.App.apptools import *
from packapp   import PackApp
from unpackapp import UnpackApp
from mtool3    import mtoolViewer


class ShellToolApp(MenuListApp):
    def start(self):
        self.menu = [
            ('Pack files',   self.pack),
            ('Unpack files', self.unpack),
            ('Test packer',  self.testpack),
            ('Mail tool',    self.mtool),
            ('Environment',  self.environ),
            ('Shell cmd',    self.command),
            ('Python cmd',   self.python),
            ('Change dir',   self.chdir),
            ('Quit',         lambda: 0) ]


    def pack(self): 
        appCall(PackApp, '-o', raw_input('Output? '), raw_input('Files? ') )


    def unpack(self):
        appCall(UnpackApp, '-i', raw_input('File? ') )


    def testpack(self):
        self.shell('diff3.py %s %s' % 
                        ( raw_input('Original? '), raw_input('New? ') ))

    def mtool(self):
        mtoolViewer(
            raw_input('mail-file? '),
            raw_input('from who ? '),
            raw_input('to who? '), 
            raw_input('cc who? '), 
            raw_input('subject? '), 
            raw_input('and-mode? (-a) ') )


    def environ(self):
        name = raw_input('Name (or <return>)? ')
        if name:
            print '%s = "%s"' % (name, self.getenv(name)) 
        else:
            for entry in self.env.items():
                print '"%s" = "%s"\n' % entry


    def command(self):
        yes = ['y', 'Y', 1, 'yes', 'YES']
        if raw_input('simple? ') in yes:
            self.shell( raw_input('Command? ') )      # can run pack,mtool too
        else:
            ans = raw_input('With input? ')
            cmd = raw_input('Command? ')
            if ans in yes:
                self.shell(cmd, 2, self.shellout)     # send last shell's output
            else:
                self.shellout = self.shell(cmd, 1)    # do popen (system+output)
                print self.shellout


    def python(self):
        import  __main__
        scope = __main__.__dict__
        exec raw_input('Command? ') in scope, scope   # not eval: allow stmts


    def chdir(self):
        import os
        os.chdir(raw_input('Dir? '))      # shell('cd x') doesn't last
    


if __name__ == '__main__':
    ShellToolApp().main()

