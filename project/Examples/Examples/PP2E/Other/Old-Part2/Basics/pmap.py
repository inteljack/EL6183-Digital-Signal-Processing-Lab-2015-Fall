import sys; map(                  # pack, the hard way
     lambda name:
        sys.stdout.write("::::::"+name+'\n' + open(name,'r').read()),
     sys.argv[1:])
