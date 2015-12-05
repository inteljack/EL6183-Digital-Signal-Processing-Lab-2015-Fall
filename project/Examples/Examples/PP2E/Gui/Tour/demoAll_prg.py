#######################################################
# 4 demo classes run as independent program processes;
# if one window is quit now, the others will live on;
# there is no simple way to run all report calls here,
# and some launch schemes drop child program stdout;
#######################################################

from Tkinter import *
demoModules = ['demoDlg', 'demoRadio', 'demoCheck', 'demoScale']
from PP2E.launchmodes import PortableLauncher

for demo in demoModules:                        # see Parallel System Tools
    PortableLauncher(demo, demo+'.py')()        # start as top-level programs

Label(text='Multiple program demo', bg='white').pack()
mainloop()
