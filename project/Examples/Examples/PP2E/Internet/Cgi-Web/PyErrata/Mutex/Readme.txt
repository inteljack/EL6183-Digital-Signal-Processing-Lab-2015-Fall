This directory contains the mutexcntl.py utility
module, as well as scripts to test it.  Run the
launch-mutex* scripts from the command line to test
the mutex class (see test.log for results).  Run
the launch-test* script to test basic flock() calls 
without the mutexcntl module.  Shared.txt is the 
shared resource, and test.lck is the lock file;
Shared.txt is analogous to a shared shelve file.
The test* scripts simulate readers and writers,
much like browse/submit CGI script processes.
