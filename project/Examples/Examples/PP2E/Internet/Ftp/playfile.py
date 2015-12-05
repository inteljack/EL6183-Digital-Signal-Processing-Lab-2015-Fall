#!/usr/local/bin/python
################################################# 
# Try to play an arbitrary audio file.
# This may not work on your system as is; it
# uses audio filters on Unix, and filename 
# associations on Windows via the start command
# line (i.e., whatever you have on your machine 
# to run *.au files--an audio player, or perhaps
# a web browser); configure me as needed.  We
# could instead launch a web browser here, with 
# LaunchBrowser.py.  See also: Lib/audiodev.py.
#################################################

import os, sys
sample = 'sousa.au'  # default audio file

unixhelpmsg = """
Sorry: can't find an audio filter for your system!
Add an entry for your system to the "unixfilter" 
dictionary in playfile.py, or play the file manually.
"""

unixfilter = {'sunos5':  '/usr/bin/audioplay',
              'linux2':  '<unknown>',
              'sunos4':  '/usr/demo/SOUND/play'}

def playfile(sample=sample):
    """
    play an audio file: use name associations 
    on windows, filter command-lines elsewhere
    """
    if sys.platform[:3] == 'win':
        os.system('start ' + sample)   # runs your audio player
    else:
        if not (unixfilter.has_key(sys.platform) and 
                os.path.exists(unixfilter[sys.platform])):
            print unixhelpmsg
        else:
            theme = open(sample, 'r')             
            audio = os.popen(unixfilter[sys.platform], 'w')  # spawn shell tool
            audio.write(theme.read())                        # send to its stdin

if __name__ == '__main__': playfile()
