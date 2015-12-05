import sys, string
sum = 0
while 1:
    line = sys.stdin.readline()
    if not line: break
    sum = sum + string.atoi(line[:-1])  
print sum
