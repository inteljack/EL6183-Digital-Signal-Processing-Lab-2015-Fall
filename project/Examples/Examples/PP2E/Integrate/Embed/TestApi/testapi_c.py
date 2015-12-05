# how to reload in Python, 
# like testapi.c does in C

import testapi, traceback
for i in range(5):
    try:
        reload(testapi)
        res = testapi.func(4, 8)
    except: 
        print 'error'
        traceback.print_exc()
    else: print res
    if i < 4: raw_input('change testapi.py now...')

