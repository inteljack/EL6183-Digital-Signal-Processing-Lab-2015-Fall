import sys
from HTMLgen import *

p = Paragraph('Making pages from objects is easy.\n')
p.append('Special < characters > are & escaped')

choices = ['tools', ['python', 'c++'], 'food', ['spam', 'eggs']]
l = List(choices)

s = SimpleDocument(title="HTMLgen 101")
s.append(Heading(1, 'Basic tags'))
s.append(p)
s.append(l)
s.append(HR())
s.append(Href('http://www.python.org', 'Python home page'))

if len(sys.argv) == 1:
    print s                 # send html to sys.stdout or real file
else:
    open(sys.argv[1], 'w').write(str(s))
