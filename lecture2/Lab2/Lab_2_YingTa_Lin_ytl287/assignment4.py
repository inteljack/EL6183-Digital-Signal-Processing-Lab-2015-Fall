import struct

#What hexadecimal symbol string gives -1 as a signed 16-bit integer using unpack() command?
k=[]
a = struct.pack('>h',-1)
struct.unpack('h','\xff\xff')
#hex( hex(ord(ans[0]))<<10 | hex(ord(ans[0])) ) <- working on this
print 'The hexdecimal symbol for -1 is FFFF'
for r in a:
    k.append(r)
print k

#What hexadecimal symbol string gives 256 as a signed 16-bit integer using unpack() command?
struct.pack('>h',256)
print 'The hexdecimal symbol for 256 is 0100'

#What hexadecimal symbol strings give the above numbers as signed 32-bit integers using unpack() command?
struct.pack('>i',-1)
struct.pack('>i',256)
print 'The hexdecimal symbol for -1 in signed 32 bit is FFFFFFFF'
print 'The hexdecimal symbol for 256 in signed 32 bit is 00000100'

#Change the value of gain to a larger number (e.g.  400000, 800000 or even larger).
#What happens? What error do you get?
print 'Changing the gain will change the volume. If\
exceed the maximum value of short integer. The maximum gain for this system is 10173.8'
