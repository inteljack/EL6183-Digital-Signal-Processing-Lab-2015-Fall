#!/bin/csh
##########################################################
# we need scripttools.py from '..', but there is a 
# cinterface.py in '.', and a cinterface.so in '..'; 
# to make sure we find the .py version in '.' when C
# or Python import 'cinterface', we can either:
# - tweak PYTHONPATH (put '.' before '..'), or 
# - make the paths explicit with module package imports;
# we use a PYTHONPATH approach here; note that the path
# can be set by sourcing this file, or manually changing 
# sys.path in main1.c (see the Embed/Inventory example);
##########################################################

source $PP2EHOME/PP2E/Config/setup-pp-embed.csh
setenv PYTHONPATH .:..:$PYTHONPATH

