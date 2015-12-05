############################################################
# start up 5 copies of child.py running in parallel;
# - on Windows, os.system always blocks its caller, 
#   and os.popen currently fails in a GUI programs
# - using DOS start command pops up a DOS box (which goes 
#   away immediately when the child.py program exits)
# - running child-wait.py with DOS start, 5 independent
#   DOS console windows popup and stay up (1 per program)
# DOS start command uses file name associations to know 
# to run Python on the file, as though double-clicked in 
# Windows explorer (any file name can be started this way);
############################################################

import os, sys
 
for i in range(5):
    #print os.popen('python child.py ' + str(i)).read()[:-1]
    #os.system('python child.py ' + str(i))
    #os.system('start child.py ' + str(i))
     os.system('start child-wait.py ' + str(i))
print 'Main process exiting.'
