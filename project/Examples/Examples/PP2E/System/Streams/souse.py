def seuss(letter, repeat):
    line = '=>'
    while 1:
        next = raw_input('Word? ')            # read from stdin
        if not next:                          # until blank line
            break
        else:
            line = line + ' ' + next
    print line + ((', ' + letter) * repeat)   # write to stdout
