#!/usr/local/bin/python
# to test the embedded-code script, without the enclosing C app 

import validate2                   # get validation function
import inventory                   # inventory, buyers
import traceback                   # stack dump on errors
from ordersfile import orders      # [(product, quant, buyer)]
                                   # no namespace or script here
for order in orders: 
    print '\n', orders.index(order), order
    try:
        (warnings, errors) = apply(validate2.validate, order)  
    except:
        print 'error in embedded function:'
        traceback.print_exc()
        continue
    print 'errors:  ', errors   or 'none'
    print 'warnings:', warnings or 'none'
    inventory.print_files()
