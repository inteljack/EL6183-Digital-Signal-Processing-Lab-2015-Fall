import sys
bytes = open(sys.argv[1], 'rb').read()
print '-'*40
print repr(bytes)

print '-'*40
while bytes:
    bytes, chunk = bytes[4:], bytes[:4]          # show 4-bytes per line
    for c in chunk: print oct(ord(c)), '\t',     # show octal of binary value
    print 

print '-'*40
for line in open(sys.argv[1], 'rb').readlines():
    print repr(line)

