################################################################################
# redirect i/o to class objects
# instances of these classes can be used anywhere a file object is expected;
# Note: we could reset/restore streams here instead of in App, but these
# classes are useful outside App, and are independant of App streams;
# there are  probably more efficient representations for the file strings;
# Beginning with Python 1.4 or so--See also standard StringIO lib module;
################################################################################

import string

class FakeStream:
    def close(self):                     # to do: seek(), tell()...
        pass                             # as is: can't back up in file
    def flush(self):
        pass                             # pass: returns None
    def isatty(self):
        return 0

class Input(FakeStream):
    def __init__(self, input):           # input: any sliceable object,
        self.text = input                # but find/getargs want real strings

    def read(self, *size):
        if not size:
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:size[0]], self.text[size[0]:]
        return res

    def readline(self):
        eoln = string.find(self.text, '\n')
        if eoln == -1: 
            res, self.text = self.text, ''
        else:
            res, self.text = self.text[:eoln+1], self.text[eoln+1:]
        return res

    def readlines(self):
        res = []
        while 1:
            line = self.readline()
            if not line: break
            res.append(line)
        return res

class Output(FakeStream):
    def __init__(self):                            # output in self.output.text
        self.text = ''
    def write(self, string):
        self.text = self.text + string             # to do: handle errors here
    def writelines(self, lines):
        for line in lines: self.write(line)        # or use joinfields

