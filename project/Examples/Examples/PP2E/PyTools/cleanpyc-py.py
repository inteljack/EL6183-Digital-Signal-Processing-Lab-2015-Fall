###########################################################
# find and delete all "*.pyc" bytecode files at and below
# the directory where this script is run; this uses a 
# Python find call, and so is portable to most machines;
# run this to delete .pyc's from an old Python release;
# cd to the directory you want to clean before running;
###########################################################

import os, sys, find              # here, gets PyTools find

count = 0
for file in find.find("*.pyc"):   # for all file names
    count = count + 1
    print file
    os.remove(file)

print 'Removed %d .pyc files' % count

