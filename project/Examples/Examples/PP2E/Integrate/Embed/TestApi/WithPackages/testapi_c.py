# package import version
# how to reload in Python, 
# like testapi.c does in C

import pkgdir.testapi, traceback 
for i in range(5):
    try:
        reload(pkgdir.testapi)
        res = pkgdir.testapi.func(4, 8)
    except: 
        print 'error'
        traceback.print_exc()
    else: print res
    if i < 4: raw_input('change pkgdir/testapi.py now...')

