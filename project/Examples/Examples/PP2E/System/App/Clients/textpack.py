#!/usr/local/bin/python
import sys                          # load the system module
marker = ':'*10 + 'textpak=>'       # hopefully unique separator

def pack():
    for name in sys.argv[1:]:       # for all command-line arguments
        input = open(name, 'r')     # open the next input file
        print marker + name         # write a separator line
        print input.read(),         # and write the file's contents

if __name__ == '__main__': pack()   # pack files listed on cmdline
