####################################################### 
# register for and handle event callbacks from C;
# compile C code, and run with 'python register.py'
####################################################### 

#
# C calls these Python functions; 
# handle an event, return a result
#

def callback1(label, count):
    return 'callback1 => %s number %i' % (label, count)

def callback2(label, count):
    return 'callback2 => ' +  label * count

#
# Python calls a C extension module 
# to register handlers, trigger events 
#

import cregister

print '\nTest1:'
cregister.setHandler(callback1)
for i in range(3):
    cregister.triggerEvent()         # simulate events caught by C layer

print '\nTest2:'
cregister.setHandler(callback2)
for i in range(3):
    cregister.triggerEvent()         # routes these events to callback2 
