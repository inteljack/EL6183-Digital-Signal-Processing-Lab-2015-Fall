#!/usr/local/bin/python

#############################################################################
# mail-tool, version 2
# extract mail message by header matches
# to do: MMDH format (startMessage():'\1\1\1\1\n')
# to do: header-line continuations (first = whitespace)
#
# example use:
# mtool.py \* andy ~/mbox
# mtool.py steveo mlutz ~/mbox msgs
#
# mtoolapp.py -i ~/mbox -t andy
# mtoolapp.py -a -f steveo -t lutz -i ~/mbox -o msgs
#
# mtoolapp.py -t andy -i ~/mbox -o -
# mtoolapp.py -i ~/mbox -t andy -o - | diff - mtool.out 
# cat ~/mbox | mtoolapp.py -i - -t andy -o - | diff - mtool.out
#
# from mtoolapp import *
# mtoolViewer('/home/lutz/mbox', 'steveo', 'lutz')
#
# from app import *
# appCall(MtoolApp, '-x', '-i', '/home/lutz/mbox', '-t', 'steveo')
# appRun('mtoolapp.py', '-i', '/home/lutz/mbox', '-f', 'andy', '-o', '-')
# ScriptOutput(...).read()
#############################################################################

import string
from PP2E.System.App.apptools import StreamApp, appCall, Output

class MtoolApp(StreamApp):
    mpath = '/usr/spool/mail/'
    sepln = 'MtoolApp' + ('#' * 64) + 'MtoolApp\n'

    def help(self):
        StreamApp.help(self) 
        for arg in [
            '-f <from-pattern>', 
            '-t <to-pattern>',
            '-c <cc-pattern>',
            '-s <subject-pattern>',
            '-x (function mode: overrides -o)',
            '-a (and mode: default=or)']: print arg

    def internalOutput(self):
        self.output = Output()
        self.output_name = '<internal>'

    def start(self):
        if not self.args:
            self.help() 
            self.exit()
        else:
            self.selects = [
                ('From ',     self.getarg('-f')),
                ('To: ',      self.getarg('-t')),
                ('Cc: ',      self.getarg('-c')),
                ('Subject: ', self.getarg('-s'))   
            ]
            self.andMode  = self.getopt('-a')
            self.funcMode = self.getopt('-x')
            self.setInput(self.mpath + self.getenv('USER'))
            if self.funcMode:
                self.internalOutput()
            else:
                self.setOutput('mtool.out')
            self.endargs()

    def eliminates(self, line):
        if self.andMode:
            for (start, patt) in self.selects:
                if (patt and
                    line[:len(start)] == start and
                    string.find(line, patt, len(start)) < 0):    # or regex
                       return 1                                  # patt !found
                                                 
    def qualifies(self, line):
        if not self.andMode:
            for (start, patt) in self.selects:
                if (patt and
                    line[:len(start)] == start and
                    string.find(line, patt, len(start)) >= 0):   # or regex
                       return 1                                  # patt found 

    def run(self):
        line = self.readline()
        while line:
            if line[:5] == 'From ':
                prefix = [self.sepln]
                match  = self.andMode
                while line:
                    if self.qualifies(line):
                        match = 1
                        break
                    if self.eliminates(line):
                        match = 0
                        break
                    if line == '\n':
                        break
                    prefix.append(line)
                    line = self.readline()
                if match:
                    self.writelines(prefix)
                    while line:
                        self.write(line)
                        line = self.readline()
                        if line[:5] == 'From ': break
                    continue
            line = self.readline()

    def stop(self):
        if not self.funcMode:
            self.message('mtool finished: see "%s".' % self.output_name)
        else:
            return string.splitfields(self.output.text, self.sepln)[1:]


#############################################################################
# to run from another program (gui...)
# mtoolViewer('/home/lutz/mbox', 'steveo', 'lutz', 0, 0, 1)
# pdb.run("mtoolCall('~/mbox', 'andy', 'lutz')")
# ...b MtoolApp.start;  c;  p self.args;  s;...
#############################################################################

def mtoolCall(Mfile, From, To, Cc='', Subj='', And=1, Mtype=MtoolApp):
    cmdargs = [
        ('-i', Mfile),
        ('-f', From ),
        ('-t', To   ),
        ('-c', Cc   ),
        ('-s', Subj )]
    cmdopts = [('-a', And)]

    args = ['-x']                           # function mode
    for (opt, arg) in cmdargs:
        if arg: args.append((opt, arg))     # add passed args
    for (opt, arg) in cmdopts:
        if arg: args.append(opt)            # add passed flags
    return appCall(Mtype, args)             # use internal output

def mtoolViewer(*args):
    msgs = apply(mtoolCall, args)           # list of messages
    for msg in msgs:
        print msg; t = raw_input()          # pause between each


#############################################################################
# run mtool as a script
#############################################################################

if __name__ == '__main__': 
    MtoolApp().main() 

