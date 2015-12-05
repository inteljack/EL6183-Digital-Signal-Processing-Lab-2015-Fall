# embedded validation code, run from C
# input = args, output = return value tuple

import string             
import inventory         

def validate(product, quantity, buyer):        # function called by name 
    msgs, errs = [], []                        # via mod/func name strings 
    first, last = buyer[0], buyer[1:]          
    if first not in string.uppercase:         
        errs.append('buyer-name:' + first)   
    if buyer not in inventory.buyers():     
        msgs.append('new-buyer-added')
        inventory.add_buyer(buyer)
    validate_order(product, quantity, errs, msgs)     # mutable list args 
    return string.join(msgs), string.join(errs)       # use "(ss)" format

def validate_order(product, quantity, errs, msgs):
    if product not in inventory.skus(): 
        errs.append('bad-product') 
    elif quantity > inventory.stock(product):
        errs.append('check-quantity')
    else:
        inventory.reduce(product, quantity)
        if inventory.stock(product) / quantity < 2:
            msgs.append('reorder-soon:' + `product`)
