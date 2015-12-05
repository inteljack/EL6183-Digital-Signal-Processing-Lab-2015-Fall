#!/usr/local/bin/python
# file tools.py: collected shell-tool menu
# todo: make pack/unpack/diff3 App().main() calls
# todo: add a sumbmenu for the last few items


from PP2E.System.App.apptools import *
from mtool2 import mtoolViewer


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
        self.shell('pack.py -b %s %s' % 
                        ( raw_input('Output? '), raw_input('Files? ') ))

    def unpack(self):
        self.shell('unpack.py %s' % raw_input('File? '))


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
            self.shell( raw_input('Command? ') ) 
        else:
            ans = raw_input('With input? ')
            cmd = raw_input('Command? ')
            if ans in yes:
                self.shell(cmd, 2, self.shellout)     # send last shell's output
            else:
                self.shellout = self.shell(cmd, 1)    # do popen (system + output)
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





##################################################################################
# debugging this:  (forgot 'self' param in App.shell method)
#
# ==>5
# With input? n
# Command? ls
# what? "5"?
# try again...
# 
# > python
# Python 1.1 (Jan 31 1995)
# Copyright 1991-1994 Stichting Mathematisch Centrum, Amsterdam
# >>> import pdb  
# >>> import tools
# >>> pdb.run("tools.ShellToolApp().main()")
# > <string>(0)?
# (Pdb) b tools.ShellToolApp.command
# (Pdb) c
# > <string>(1)?
# (Pdb) c
#  
#        MENU...
#                0) Pack files
#                1) Unpack files
#                2) Test packer
#                3) Mail tool
#                4) Environment
#                5) Shell tool
#                6) Quit
# ==>5
# > ./tools.py(49)command(<ShellToolApp...ance at a8a80>,): def command(self):
# (Pdb) s
# > ./tools.py(50)command(<ShellToolApp...ance at a8a80>,): ans = raw_input('With input? ')
# (Pdb) s
# With input? n
# > ./tools.py(51)command(<ShellToolApp...ance at a8a80>,): cmd = raw_input('Command? ')
# (Pdb) s
# Command? ls
# > ./tools.py(52)command(<ShellToolApp...ance at a8a80>,): if ans in ['y', 'Y']:
# (Pdb) s
# > ./tools.py(55)command(<ShellToolApp...ance at a8a80>,): self.shellout = self.shell(cmd, 1)    # do popen (system + output)
# (Pdb) s
# > ./app.py(102)shell(<ShellToolApp...ance at a8a80>, 'ls', 1): def shell(command, fork=0, inp=''):
# (Pdb) s
# > ./app.py(103)shell(<ShellToolApp...ance at a8a80>, 'ls', 1): if not fork:
# (Pdb) p fork
# 'ls'
# (Pdb) p command
# <ShellToolApp instance at a8a80>
# (Pdb) q
###################################################################################

