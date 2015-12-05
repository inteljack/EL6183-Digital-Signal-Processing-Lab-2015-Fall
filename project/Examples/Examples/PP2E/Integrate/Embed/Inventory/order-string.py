#!/usr/local/bin/python
# to test the embedded-code script, without the enclosing C app 

import inventory                   # inventory, buyers
import traceback                   # stack dump on errors
from ordersfile import orders      # [(product, quant, buyer)]

names  = {}                                    # namespace dict
script = open('validate1.py', 'r').read()      # load code-string
for order in orders:
    print '\n', orders.index(order), order
    names['PRODUCT'], names['QUANTITY'], names['BUYER'] = order
    try:
        exec script in names, names
    except:
        print 'error in embedded code:'
        traceback.print_exc()
        continue
    print 'errors:  ', names['ERRORS']   or 'none'
    print 'warnings:', names['WARNINGS'] or 'none'
    inventory.print_files()
