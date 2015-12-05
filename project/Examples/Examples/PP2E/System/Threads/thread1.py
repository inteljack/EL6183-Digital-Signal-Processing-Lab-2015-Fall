# spawn threads until you type 'q'

import thread

def child(tid):
    print 'Hello from thread', tid

def parent():
    i = 0
    while 1:
        i = i+1
        thread.start_new(child, (i,))
        if raw_input() == 'q': break

parent()
