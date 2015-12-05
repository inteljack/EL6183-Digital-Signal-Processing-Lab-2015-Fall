#!/usr/local/bin/python

################################################################################
# Test i/o redirection apps: 4 class levels, with i/o classes embedded.
# also: see Lib/StringIO.py for other string i/o (seek, tell..)
# also: see mtoolapp.py, packapp.py, unpackapp.py for other clients
################################################################################

import sys
from PP2E.System.App.apptools import *

def _self_test():
    print raw_input('here we go => ')

    def testfunc(N):
        ans = raw_input('Enter? ')               # from an Input instance
        for i in range(N):
            print ans                            # to an Output instance
        sys.stdout.write(sys.stdin.readline())   # from Input, to Output
        print "Ni!" * N

    input  = 'Spam!\nA shrubbery...\n'
    output = redirected(input, testfunc, (5,))   # make/run a FuncTestApp

    ans = raw_input('welcome back => ')
    print 'got it =>', ans                       # stdin, stdout reset?
    print 'testfunc output =>\n', output

    def tee(): 
        sys.stdout.writelines(sys.stdin.readlines())

    def tee2():
        text = sys.stdin.readlines()
        print text
        for line in text:
            sys.stdout.write('> ')
            print line,

    # more FuncTestApp's
    print 'tee output =>\n',  redirected("spam\nSpam\nSPAM!\n", tee,  ())
    print 'tee2 output =>\n', redirected("spam\nSpam\nSPAM!",   tee2, ()) 

    # more subclasses
    class EchoApp(TestInteractiveApp):
        def evalCommand(self, command):
            return 'got this -> ' + string.upper(command)

    output = EchoApp("guido\nis\ngod\n").main() 
    print 'EchoApp output =>\n', output

    class DemoApp(TestMenuApp):
        menu = {
            'hello' : lambda: 'Hello world!',
            'play'  : lambda: 'Ni' * 4,   
            'bye'   : lambda: 0,
        }

    output = DemoApp("hello\nspam\nplay\nbye").main()
    print 'DemoApp output =>\n', output
    
if __name__ == '__main__': _self_test()         # when run at top-level
