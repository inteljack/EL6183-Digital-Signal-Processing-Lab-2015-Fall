############################################################
# spawn threads to watch shared global memory change;
# threads normally exit when the function they run returns, 
# but thread.exit() can be called to exit calling thread;
# thread.exit is same as sys.exit and raising SystemExit;
# threads communicate with possibly-locked global vars;
############################################################

import thread                                   
exitstat = 0 

def child():
    global exitstat                               # process global names
    exitstat = exitstat + 1                       # shared by all threads
    threadid = thread.get_ident()
    print 'Hello from child', threadid, exitstat
    thread.exit()
    print 'never reached'

def parent():
    while 1:
        thread.start_new_thread(child, ())
        if raw_input() == 'q': break

parent()
