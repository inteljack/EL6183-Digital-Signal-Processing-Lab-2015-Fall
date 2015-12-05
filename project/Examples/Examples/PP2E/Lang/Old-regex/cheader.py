#! /usr/local/bin/python
import sys, regex, string

# patt_define  matches:  "#define name ..."
# patt_macro   matches:  "#define name(arg) ..."
# patt_include matches:  "#include (<|")name/name/name.name..."

patt_define = regex.compile(
  '^#[\t ]*define[\t ]+\([a-zA-Z0-9_]+\)[\t ]*')

patt_macro = regex.compile(
  '^#[\t ]*define[\t ]+\([a-zA-Z0-9_]+\)(\([_a-zA-Z][_a-zA-Z0-9]*\))[\t ]+')

patt_include = regex.compile(
  '^#[\t ]*include[\t ]+[<"]\([a-zA-Z0-9_/\.]+\)')

def scan(file):
    lineno = 0
    while 1:                           # scan input file line-by-line
        line = file.readline()
        if not line: break
        lineno = lineno + 1
        n = patt_macro.match(line)
        if n >= 0:
            line, lineno = cont(file, line, lineno)
            name, arg = patt_macro.group(1, 2)     # two matched substrings
            body = line[n:]
            print '%d) %s[%s] = %s' % (lineno, name, arg, string.strip(body))
            continue

        n = patt_define.match(line)                # save length-of-match
        if n >= 0:
            line, lineno = cont(file, line, lineno)
            name = patt_define.group(1)            # substring for \(...\)
            body = line[n:]
            print '%d) %s = %s' % (lineno, name, string.strip(body) or None)
            continue

        if patt_include.match(line) >= 0:
            regs = patt_include.regs               # start/stop indexes
            a, b = regs[1]                         # for nested patterns
            filename = line[a:b]                   # slice out of line
            print '%d) include %s' % (lineno, filename)

def cont(file, line, lineno):
    while line[-2:] == '\\\n': 
        next = file.readline()      # merge continuation lines
        if not next: break
        line, lineno = line[:-2]+next, lineno+1
    return line, lineno

if len(sys.argv) == 1:
    scan(sys.stdin)                 # no args: read stdin
else:
    scan(open(sys.argv[1], 'r'))    # arg: input file name
