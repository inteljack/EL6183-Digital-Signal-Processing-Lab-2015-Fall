#!/usr/bin/python
import os, time
from mutexcntl import MutexCntl

class app(MutexCntl):
    def go(self):
        self.filename = 'test'
        print os.getpid(), 'start mutex writer'
        self.exclusiveAction(self.update)               # must do this alone;
                                                        # no update or report
    def update(self):                                   # can run at same time
        print os.getpid(), 'got write lock'
        log = open('Shared.txt', 'a')
        time.sleep(3)
        log.write('%d Hello\n' % os.getpid())
        print os.getpid(), 'unlocking\n'

if __name__ == '__main__': app().go()

