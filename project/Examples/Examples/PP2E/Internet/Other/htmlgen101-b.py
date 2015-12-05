import sys
from HTMLgen import *
d = SimpleDocument(title="HTMLgen 101 B")

# show this script
text = open('htmlgen101-b.py', 'r').read()
d.append(Heading(1, 'Source code')) 
d.append(Paragraph( PRE(text) )) 

# add gif and links 
site  = 'http://www.python.org'
gif   = 'PythonPoweredSmall.gif'
image = Image(gif, alt='picture', align='left', hspace=10, border=0)

d.append(HR())
d.append(Href(site, image))
d.append(Href(site, 'Python home page'))

if len(sys.argv) == 1:
    print d  
else:
    open(sys.argv[1], 'w').write(str(d))
