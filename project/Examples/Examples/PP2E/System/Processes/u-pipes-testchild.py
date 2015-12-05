import os, time, sys 
mypid     = os.getpid()
parentpid = os.getppid()
sys.stderr.write('Child %d of %d got arg: %s\n' % 
                                (mypid, parentpid, sys.argv[1]))
for i in range(2):
    time.sleep(3)             # make parent process wait by sleeping here 
    input = raw_input()       # stdin tied to pipe: comes from parent's stdout
    time.sleep(3)
    reply = 'Child %d got: [%s]' % (mypid, input)
    print reply               # stdout tied to pipe: goes to parent's stdin 
    #sys.stdout.flush()        # make sure it's sent now else blocks
