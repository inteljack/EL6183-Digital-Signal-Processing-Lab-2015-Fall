#!/usr/local/bin/python
 
############################################### 
# Usage: % sousa.py
# Fetch and play the Monty Python theme song.
# Inspired by an idea from Jeff Bauer.
#
# This may not work on your system as is: it 
# requires a machine with ftp access, and uses
# Sun audio filters. Configure as needed.
###############################################
 
import os, sys
from ftplib import FTP             # socket-based ftp tools
from posixpath import exists       # file existence test
 
sample = 'sousa.au'
filter = {'sunos5': '/usr/bin/audioplay', 
          'linux1': '<unknown>',
          'sunos4': '/usr/demo/SOUND/play'}

helpmsg = """
Sorry: can't find an audio filter for your system!
Add an entry to the script's "filter" dictionary for
your system's audio command, or run the ftp code and
use the ".au" file. Also see module: Lib/audiodev.py.
"""

# check the filter 
if filter.has_key(sys.platform) and exists(filter[sys.platform]):
    print 'Working...'
else:
    print helpmsg    
    sys.exit(1)

# ftp the audio file
if not exists(sample):
    theme = open(sample, 'w')
    ftp = FTP('ftp.python.org')       # connect to ftp site
    ftp.login()                       # use anonymous login
    ftp.cwd('pub/python/misc')
    ftp.retrbinary('RETR ' + sample, theme.write, 1024)
    ftp.quit()
    theme.close()
 
# send it to audio device
theme = open(sample, 'r')             
audio = os.popen(filter[sys.platform], 'w')    # spawn shell tool
audio.write(theme.read())                      # send to stdin
