#!/usr/bin/python
import os, time
from mutexcntl import MutexCntl

class app(MutexCntl):
    def go(self):
        self.filename = 'test'
        print os.getpid(), 'start mutex reader'
        self.sharedAction(self.report)                # can report with others
                                                      # but not during update
    def report(self):
        print os.getpid(), 'got read lock'
        time.sleep(3)
        print 'lines so far:', os.popen('wc -l Shared.txt').read(),
        print os.getpid(), 'unlocking\n'

if __name__ == '__main__': app().go()
