def scanner(name, function): 
    file = open(name, 'r')              # create a file object
    while 1:
        line = file.readline()          # call file methods
        if not line: break              # until end-of-file
        function(line)                  # call a function object
    file.close() 
