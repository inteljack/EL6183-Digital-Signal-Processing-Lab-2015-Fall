#!/usr/local/bin/python

#############################################################################
# mail-tool, version 3
# adds: MMDH format (startMessage():'\1\1\1\1\n')
# adds: header-line continuations (first = whitespace)
#
# note: '-x' here forces internal-output, and a return value
# in stop().  This is an alternative to subclassing with a 
# 'mixin' class that provides internal output (see app.py)
#############################################################################

import string
from PP2E.System.App.apptools import App, appCall
[BODY, HEADER] = range(2)

class MtoolApp(App):
    mpath  = '/usr/spool/mail/'
    marker = 'MtoolApp' + ('#' * 64) + 'MtoolApp\n'

    def help(self):
        App.help(self) 
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
            self.setInput(self.mpath + self.getenv('USER'))        # or -i
            if self.funcMode:
                self.internalOutput()
            else:
                self.setOutput('mtool.out') 			   # or -o
            self.endargs()
            self.context = BODY
            self.peek    = ''

    def eliminates(self, line):
        if self.andMode:
            for (start, patt) in self.selects:
                if (patt and
                    line[:len(start)] == start and
                    string.find(line, patt, len(start)) < 0):     # regex.search
                       return 1                                   # patt !found
                                                                  # or ret None
    def qualifies(self, line):
        if not self.andMode:
            for (start, patt) in self.selects:
                if (patt and
                    line[:len(start)] == start and
                    string.find(line, patt, len(start)) >= 0):    # regex.search
                       return 1                                   # patt found 

    def startHeader(self, line):			# subclass hooks
        return line[:5] == 'From '             		# unix mbox

    def stopHeader(self, line):
        return line == '\n'    	                 	# unix mbox

    def contHeader(self, char):
        return char in [' ', '\t']                 	# unix mbox

    def nextline(self):					# physical line
        line = self.peek
        if line != '\n':
            line = line + App.readline(self)		# '' on eof
        self.peek = self.read(1)
        return line

    def readline(self):					# logical line
        line = self.nextline()				# or: sept class
        if self.context == BODY:
            if self.startHeader(line):
                self.context = HEADER
        else:
            if self.stopHeader(line):
                self.context = BODY
        if self.context == HEADER:
            while self.contHeader(self.peek):
                line = line + self.nextline()
        return line

    def run(self):
        line = self.readline()
        while line:
            if self.startHeader(line):
                prefix = [self.marker]
                match  = self.andMode
                while line:
                    if self.stopHeader(line):
                        break
                    if self.qualifies(line):
                        match = 1
                        break
                    if self.eliminates(line):
                        match = 0
                        break
                    prefix.append(line)
                    line = self.readline()
                if match:
                    self.writelines(prefix)
                    while line:
                        self.write(line)
                        line = self.readline()
                        if self.startHeader(line): break
                    continue
            line = self.readline()

    def stop(self):
        if not self.funcMode:
            self.message('mtool finished: see "%s".' % self.output_name)
        else:
            return string.splitfields(self.output.text, self.marker)[1:]


#############################################################################
# subclass for a different mbox format...
#############################################################################

class MtoolMMDH(MtoolApp):
    def startHeader(self, line):
        return line[:5] == '\1\1\1\1\n'


#############################################################################
# run from another program (gui...)
#############################################################################

def mtoolCall(Mfile, From, To, Cc='', Subj='', And=1, Mtype=MtoolApp):
    cmdargs = [
        ('-i', Mfile),
        ('-f', From ),
        ('-t', To   ),
        ('-c', Cc   ),
        ('-s', Subj )]
    cmdopts = [('-a', And)]

    args = ['-x']			    # function mode
    for (opt, arg) in cmdargs:
        if arg: args.append((opt, arg))

    for (opt, arg) in cmdopts:
        if arg: args.append(opt)
                        
    return appCall(Mtype, args)             # internal output


def mtoolViewer(*args):
    msgs = apply(mtoolCall, args)
    for msg in msgs:
        print msg; t = raw_input()          # pause between each


#############################################################################
# run mtool as a script
#############################################################################

if __name__ == '__main__': 
    MtoolApp().main() 

