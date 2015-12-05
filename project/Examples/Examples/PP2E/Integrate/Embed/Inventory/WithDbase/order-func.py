#!/usr/local/bin/python
# to test the embedded-code script, without the enclosing C app 

import sys   
sys.path.append('..')              # get validate2 from above

import validate2                   # get validation function
import inventory                   # inventory, buyers
import traceback                   # stack dump on errors

if len(sys.argv) == 1:
    ofile = 'Data/ordersfile.data'
else:
    ofile = 'Data/' + sys.argv[1]
orders = inventory.load_orders(ofile)
print orders

inventory.print_files()
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
