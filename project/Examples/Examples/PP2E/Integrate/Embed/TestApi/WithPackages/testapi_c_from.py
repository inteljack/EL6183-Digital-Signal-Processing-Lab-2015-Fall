# package import version, from
# how to reload in Python, 
# like testapi.c does in C

import pkgdir.testapi, traceback                 # get mod name: from doesn't
for i in range(5):
    try:
        reload(pkgdir.testapi)                   # still need to reload
        from pkgdir.testapi import func          # get new name binding
        res = func(4, 8)
    except: 
        print 'error'
        traceback.print_exc()
    else: print res
    if i < 4: raw_input('change pkgdir/testapi.py now...')

