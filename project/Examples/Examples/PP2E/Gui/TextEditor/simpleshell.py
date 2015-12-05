namespace= {}
while 1:
    try:
        line = raw_input('>>> ')      # single line statements only
    except EOFError:
        break
    else:
        exec line in namespace        # or eval() and print result
