# run me standalone to initialize the database files

import shelve, pickle
inventoryFile = 'Dbase/dbinventory'
buyerFile     = 'Dbase/dbbuyers'

def dbase_init():
    Inventory = shelve.open(inventoryFile, 'c')
    Inventory['111'] = 10
    Inventory['555'] = 1
    Inventory['444'] = 100
    Inventory['222'] = 5                    # keys are strings
    Inventory.close()                       # vals are integers

    Buyers = open(buyerFile, 'w')
    pickle.dump(['GRossum', 'JOusterhout', 'LWall'], Buyers)
    Buyers.close()

if __name__ == '__main__': dbase_init()

