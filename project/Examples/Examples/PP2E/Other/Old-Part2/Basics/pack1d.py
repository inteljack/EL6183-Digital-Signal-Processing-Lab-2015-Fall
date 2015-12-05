#!/usr/local/bin/python
from sys import *
for name in argv[1:]:     
    print '::::::' + name + '\n', open(name, 'r').read(), 
