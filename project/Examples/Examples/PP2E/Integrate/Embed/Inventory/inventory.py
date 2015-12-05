# simulate inventory/buyer databases while prototyping

Inventory = { 111: 10,           # "sku (product#) : quantity"
              555: 1,            # would usually be a file or shelve:
              444: 100,          # the operations below could work on 
              222: 5 }           # an open shelve (or dbm file) too...

Skus = Inventory.keys()          # cache keys if they won't change

def skus():           return Skus
def stock(sku):       return Inventory[sku]
def reduce(sku, qty): Inventory[sku] = Inventory[sku] - qty

Buyers = ['GRossum', 'JOusterhout', 'LWall']   # or keys() of a shelve|dbm file

def buyers():         return Buyers
def add_buyer(buyer): Buyers.append(buyer)

def print_files():
    print Inventory, Buyers     # check updates effect

