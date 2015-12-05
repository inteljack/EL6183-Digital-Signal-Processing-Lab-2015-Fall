############################################################################
# implement inventory/buyer databases as persistent shelve/pickle files;
# since the validations are already coded to use a function call interface,
# we just map those calls back to the shelve or pickled object here--no 
# need to change validations code;  caveat: some dbm flavors may need a 
# Inventory.close() call, and this scheme doesn't support concurrent dbase
# access--shelves must be locked if concurrent access is possible (see 
# flock() in the PyErrata example in the Internet chapter), and we would
# want to load the Buyers list from its file on each buyers() call;
#
# note that shelves require string keys (not ints), but we load raw
# strings from the order data file, so no conversions are necessary here;
# Buyers could be a shelve with all values = None if the list grows long:
# that would replace the 'in' test with a shelve index (but may be slower,
# since it adds a file access);  Inventory could almost be a simple dbm 
# file instead of a shelve, but that requires mapping integer values to 
# and from strings (dbm values must be strings--see persistence chapter);
############################################################################

import shelve, pickle, string
from dbasetools import inventoryFile, buyerFile


# open shelve once per process, on first
# import of this file; changes are auto
# written through to file on key assignment

Inventory = shelve.open(inventoryFile)

def skus():           
    return Inventory.keys()

def stock(sku):       
    return Inventory[sku]

def reduce(sku, qty): 
    Inventory[sku] = Inventory[sku] - qty

def closedbase():
    Inventory.close()  # if your dbm flavor requires it


# load buyers list once per process
# writes changes through to fil on changes

Buyers = pickle.load(open(buyerFile, 'r'))

def buyers():         
    return Buyers

def add_buyer(buyer): 
    Buyers.append(buyer)
    pickle.dump(Buyers, open(buyerFile, 'w'))

def print_files():
    text = ''
    for key in Inventory.keys():
        text = text + (' %s=>%d ' % (key, Inventory[key]))
    print 'Stock => {%s}' % text
    print 'Buyer =>', Buyers


# load order list from flat text file;
# converts quantity only to an integer

def load_orders(filename):
    orders = []
    for line in open(filename, 'r').readlines():
        product, quantity, buyer = string.split(line)
        orders.append( (product, string.atoi(quantity), buyer) )
    return orders

