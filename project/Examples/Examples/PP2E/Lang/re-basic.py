# literals, sets, ranges   (all print 2 = offset where pattern found)

import re                                  # the one to use today

pattern, string = "A.C.", "xxABCDxx"       # nonspecial chars match themself
matchobj = re.search(pattern, string)      # '.' means any one char
if matchobj:                               # search returns match object or None
    print matchobj.start()                 # start is index where matched

pattobj  = re.compile("A.*C.*")            # 'R*' means zero or more Rs
matchobj = pattobj.search("xxABCDxx")      # compile returns pattern obj
if matchobj:                               # patt.search returns match obj
    print matchobj.start()                     

# selection sets
print re.search(" *A.C[DE][D-F][^G-ZE]G\t+ ?", "..ABCDEFG\t..").start()

# alternatives
print re.search("A|XB|YC|ZD", "..AYCD..").start()  # R1|R2 means R1 or R2

# word boundaries
print re.search(r"\bABCD", "..ABCD ").start()      # \b means word boundary
print re.search(r"ABCD\b", "..ABCD ").start()      # use r'...' to escape '\'
