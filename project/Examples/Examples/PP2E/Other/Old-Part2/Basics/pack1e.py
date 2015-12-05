#!/usr/local/bin/python
from sys import argv
marker = ':' * 6                   # string repetition

for i in range(1, len(argv)):      # for (i=1; i < argc; i++)
    input = open(argv[i], 'r')
    print marker + argv[i]
    print input.read(),
