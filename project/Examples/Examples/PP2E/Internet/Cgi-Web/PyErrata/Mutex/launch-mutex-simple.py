#!/usr/bin/python
# launch test program processes
# same, but start mutexcntl clients

import os

for i in range(1):                
    if os.fork() == 0:           
        os.execl("./testwrite-mutex.py") 

for i in range(1):
    if os.fork() == 0:            
        os.execl("./testread-mutex.py") 

for i in range(1):
    if os.fork() == 0:            
        os.execl("./testwrite-mutex.py") 
