import regex

# literals, sets, ranges
print regex.search("A.C.", "xxABCDxx")
print regex.search(" *A.C[DE][D-F][^G-ZE]G\t+ ?", "..ABCDEFG\t..")

# line boundaries
print regex.search("[\t ]+A.CDE[^G-ZA-E]G\t+ ?$", "..  ABCDEFG\t ")

# alternatives
print regex.search("A\|XB\|YC\|ZD", "..AYCD..")

# word boundaries
print regex.search("\<ABCD", "..ABCD ")
print regex.search("ABCD\>", "..ABCD ")

# groups
x = regex.compile("A\(.\)B\(.\)C\(.\)")     # saves 3 substrings
x.match("A0B1C2")
print x.group(3) 

# backreferences
x = regex.compile("\(.\)\\1")               # repeat prior character
print x.match("AA")
print x.match("AB")     # fails: -1
