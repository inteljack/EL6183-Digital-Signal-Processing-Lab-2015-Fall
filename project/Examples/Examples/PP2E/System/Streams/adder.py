import sys, string
sum = 0
while 1:
    try:
        line = raw_input()                # or call sys.stdin.readlines():
    except EOFError:                      # or sys.stdin.readline() loop
        break
    else:
        sum = sum + string.atoi(line)     # int(line[:-1]) treats 042 as octal
print sum
