#!/usr/local/bin/python
################################################# 
# Usage: % sousa.py
# Fetch and play the Monty Python theme song.
# This may not work on your system as is: it 
# requires a machine with ftp access, and uses
# audio filters on Unix and your .au player on 
# Windows.  Configure playfile.py as needed.
#################################################
 
import os, sys
from PP2E.Internet.Ftp.getfile  import getfile
from PP2E.Internet.Ftp.playfile import playfile
sample = 'sousa.au'

getfile(sample)    # fetch audio file by ftp
playfile(sample)   # send it to audio player
