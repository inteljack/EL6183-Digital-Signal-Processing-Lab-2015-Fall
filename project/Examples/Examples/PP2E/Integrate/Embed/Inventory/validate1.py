# embedded validation code, run from C
# input vars:  PRODUCT, QUANTITY, BUYER
# output vars: ERRORS, WARNINGS

import string              # all python tools are available to embedded code
import inventory           # plus C extensions, Python modules, classes,..
msgs, errs = [], []        # warning, error message lists

def validate_order():
    if PRODUCT not in inventory.skus():      # this function could be imported
        errs.append('bad-product')           # from a user-defined module too
    elif QUANTITY > inventory.stock(PRODUCT):
        errs.append('check-quantity')
    else:
        inventory.reduce(PRODUCT, QUANTITY)
        if inventory.stock(PRODUCT) / QUANTITY < 2:
            msgs.append('reorder-soon:' + `PRODUCT`)

first, last = BUYER[0], BUYER[1:]            # code is changeable on-site:
if first not in string.uppercase:            # this file is run as one long
    errs.append('buyer-name:' + first)       # code-string, with input and
if BUYER not in inventory.buyers():          # output vars used by the C app
    msgs.append('new-buyer-added')
    inventory.add_buyer(BUYER)
validate_order()

ERRORS   = string.join(errs)      # add a space between messages
WARNINGS = string.join(msgs)      # pass out as strings: "" == none

