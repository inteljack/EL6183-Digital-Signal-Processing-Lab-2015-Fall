########################################################
# generally useful mixin, so a separate module; 
# requires self.filename attribute to be set, and 
# assumes self.filename+'.lck' file already exists;
# set mutexcntl.debugMutexCntl to toggle logging;
# writes lock log messages to self.filename+'.log';
########################################################

import fcntl, os, time
from FCNTL import LOCK_SH, LOCK_EX, LOCK_UN

debugMutexCntl = 1
processType = {LOCK_SH: 'reader', LOCK_EX: 'writer'}

class MutexCntl:
    def lockFile(self, mode):
        self.logPrelock(mode)
        self.lock = open(self.filename + '.lck')    # lock file in this process
        fcntl.flock(self.lock.fileno(), mode)       # waits for lock if needed
        self.logPostlock()

    def lockFileRead(self):                         # allow > 1 reader: shared
        self.lockFile(LOCK_SH)                      # wait if any write lock

    def lockFileWrite(self):                        # writers get exclusive lock
        self.lockFile(LOCK_EX)                      # wait if any lock: r or w

    def unlockFile(self):
        self.logUnlock()
        fcntl.flock(self.lock.fileno(), LOCK_UN)    # unlock for other processes

    def sharedAction(self, action, *args):          # higher level interface
        self.lockFileRead()                         # block if a write lock
        try:
            result = apply(action, args)            # any number shared at once
        finally:                                    # but no exclusive actions
            self.unlockFile()                       # allow new writers to run 
        return result

    def exclusiveAction(self, action, *args):
        self.lockFileWrite()                        # block if any other locks
        try:
            result = apply(action, args)            # no other actions overlap
        finally: 
            self.unlockFile()                       # allow new readers/writers
        return result

    def logmsg(self, text):
        if not debugMutexCntl: return
        log = open(self.filename + '.log', 'a')       # append to the end
        log.write('%s\t%s\n' % (time.time(), text))   # output won't overwrite
        log.close()                                   # but it may intermingle

    def logPrelock(self, mode):
        self.logmsg('Requested: %s, %s' % (os.getpid(), processType[mode]))
    def logPostlock(self):
        self.logmsg('Aquired: %s' % os.getpid())
    def logUnlock(self):
        self.logmsg('Released: %s' % os.getpid())

