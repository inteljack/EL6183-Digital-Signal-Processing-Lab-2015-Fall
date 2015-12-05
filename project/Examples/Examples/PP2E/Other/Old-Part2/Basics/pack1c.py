#!/usr/local/bin/python

from sys import argv
marker = '::::::'
output = open('pack.out', 'w')             # use a real output file

for name in argv[1:]:  
    input = open(name, 'r')                # input.close() automatic...
    output.write(marker + name + '\n')
    output.write( input.read() )           # output.close() automatic...