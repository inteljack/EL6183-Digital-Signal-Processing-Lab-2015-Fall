# groups (extract substrings matched by REs in '()' parts)

import re

patt = re.compile("A(.)B(.)C(.)")                  # saves 3 substrings
mobj = patt.match("A0B1C2")                        # each '()' is a group, 1..n
print mobj.group(1), mobj.group(2), mobj.group(3)  # group() gives substring

patt = re.compile("A(.*)B(.*)C(.*)")               # saves 3 substrings
mobj = patt.match("A000B111C222")                  # groups() gives all groups
print mobj.groups()

print re.search("(A|X)(B|Y)(C|Z)D", "..AYCD..").groups()

patt = re.compile(r"[\t ]*#\s*define\s*([a-z0-9_]*)\s*(.*)") 
mobj = patt.search(" # define  spam  1 + 2 + 3")            # parts of C #define
print mobj.groups()                                         # \s is whitespace
