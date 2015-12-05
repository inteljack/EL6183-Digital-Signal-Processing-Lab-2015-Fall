#!/usr/local/bin/python
######################################################################
# Run me to convert all text files to UNIX/Linux line-feed format.
# You only need to do this if you see odd '\r' characters at the end
# of lines in text files in this distribution, when they are viewed 
# with your text editor (e.g., vi).  This script converts all files 
# at and below the examples root, and only converts files that have  
# not already been converted (it's okay to run this multiple times).
#
# Since this is a Python script which runs another Python script, 
# you must install Python first to run this program; then from your
# system command-line (e.g., a xterm window), cd to the directory 
# where this script lives, and then type "python tounix.py".  You 
# may also be able to simply click on this file's icon in your file
# system explorer, if it knows what '.py' file are.
###################################################################### 

import os
prompt = """
This program converts all text files in the book
examples distribution to UNIX line-feed format.
Are you sure you want to do this (y=yes)? """

answer = raw_input(prompt) 
if answer not in ['y', 'Y', 'yes']:
    print 'Cancelled'
else:
    os.system('python PyTools/fixeoln_all.py tounix')
