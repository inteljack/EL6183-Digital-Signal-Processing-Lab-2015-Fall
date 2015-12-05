#!/usr/local/bin/python

import os 

# ipc exit, but pipe breaks
# os.popen("ipc2", 'r')

# ipc1 stalled...
# os.popen("ipc2", 'w')
# os.system("ipc2")

# ipc1 exits, pipe breaks...
# os.popen("ipc2 &", 'r')

# works: ipc exit, then ipc output
# os.popen("ipc2 &", 'w')
# os.system("ipc2 &")

# works
# pipe = os.popen("ipc2 &", 'r')
# res = []
# while 1:
    # line = pipe.readline()
    # if not line: break
    # res.append(line)

# same effect...
pipe = os.popen("ipc2", 'r')
res = []
while 1:
    line = pipe.readline()
    if not line: break
    res.append(line)

print res 
print 'ipc1 exit'

