####################################################
# the scanner (lexical analyser)
####################################################

import string 
SyntaxError    = 'SyntaxError'         # local errors
LexicalError   = 'LexicalError'

class Scanner:
    def __init__(self, text):
        self.next = 0
        self.text = text + '\0'         

    def newtext(self, text):
        Scanner.__init__(self, text)

    def showerror(self):
        print '=> ', self.text
        print '=> ', (' ' * self.start) + '^'
        
    def match(self, token):
        if self.token != token:
            raise SyntaxError, [token]
        else:
            value = self.value
            if self.token != '\0':
                self.scan()                  # next token/value
            return value                     # return prior value

    def scan(self):
        self.value = None
        ix = self.next
        while self.text[ix] in string.whitespace:
            ix = ix+1
        self.start = ix

        if self.text[ix] in ['(', ')', '-', '+', '/', '*', '\0']:
            self.token = self.text[ix] 
            ix = ix+1

        elif self.text[ix] in string.digits:
            str = ''
            while self.text[ix] in string.digits:
               str = str + self.text[ix] 
               ix = ix+1
            if self.text[ix] == '.':
                str = str + '.'
                ix = ix+1
                while self.text[ix] in string.digits:
                   str = str + self.text[ix] 
                   ix = ix+1
                self.token = 'num'
                self.value = string.atof(str)
            else:
                self.token = 'num'
                self.value = string.atol(str)

        elif self.text[ix] in string.letters:
            str = ''
            while self.text[ix] in (string.digits + string.letters): 
                str = str + self.text[ix]
                ix = ix+1
            if string.lower(str) == 'set':
                self.token = 'set'
            else:
                self.token = 'var'
                self.value = str  

        else:
            raise LexicalError
        self.next = ix
        
