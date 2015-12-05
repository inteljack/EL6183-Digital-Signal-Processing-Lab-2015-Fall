#!/usr/bin/python
######################################################
# launch test program processes
# run with ./launch-test.py > launch-test.out 
# try spawning reader before writer, then writer
# before reader--second process blocks till first 
# unlocks in both cases; if launches 2 readers 
# initially, both get lock and block writer; if
# launch 2 writers first then 2 readers, 2nd writer
# waits for first, both readers wait for both
# writers, and both readers get lock at same time;
# in test below, the first writer runs, then all 
# readers run before any writer;  if readers are 
# first, all run before any writer; (all on linux)
######################################################

import os

for i in range(1):
    if os.fork() == 0:            
        os.execl("./testwrite.py") 

for i in range(2):                      # copy this process
    if os.fork() == 0:                  # if in new child process
        os.execl("./testread.py")       # overlay with test program

for i in range(2):                
    if os.fork() == 0:             
        os.execl("./testwrite.py")      # same, but start writers

for i in range(2):
    if os.fork() == 0:            
        os.execl("./testread.py") 

for i in range(1):
    if os.fork() == 0:            
        os.execl("./testwrite.py") 
