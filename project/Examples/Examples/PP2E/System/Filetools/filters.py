def filter_files(name, function):         # filter file through function
    input  = open(name, 'r')              # create file objects
    output = open(name + '.out', 'w')     # explicit output file too
    for line in input.readlines():
        output.write(function(line))      # write the modified line
    input.close() 
    output.close()                        # output has a '.out' suffix

def filter_stream(function):
    import sys                            # no explicit files
    while 1:                              # use standard streams
        line = sys.stdin.readline()       # or: raw_input()
        if not line: break
        print function(line),             # or: sys.stdout.write()

if __name__ == '__main__': 
    filter_stream(lambda line: line)      # copy stdin to stdout if run
