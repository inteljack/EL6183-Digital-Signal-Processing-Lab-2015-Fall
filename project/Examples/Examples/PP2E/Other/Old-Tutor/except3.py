file = open('data', r)    # open a file (discussed later)
try:
    stuff(file)           # the file has been opened here
finally:
    file.close()          # close the file no matter what happens in stuff
