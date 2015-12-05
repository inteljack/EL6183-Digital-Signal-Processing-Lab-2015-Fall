#!/usr/local/bin/python
#########################################
# --SEE FIXEOLN FOR A BETTER SOLUTION--
# warning: only run me once, else keeps
# adding more \r's (but fixeoln* won't)
#########################################
import old_toboth                               # unix \n => dos \r\n line-end
old_toboth.convert(From="\n", To="\r\n")        # to check: oct(ord('\r'))
