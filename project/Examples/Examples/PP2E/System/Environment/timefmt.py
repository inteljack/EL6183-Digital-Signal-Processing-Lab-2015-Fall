import time
gmt = time.gmtime(time.time())
fmt = '%a, %d %b %Y %H:%M:%S GMT'
str = time.strftime(fmt, gmt)
hdr = 'Date: ' + str
print hdr

# C:\testdir>python timefmt.py
# Date: Fri, 02 Jun 2000 16:46:27 GMT
