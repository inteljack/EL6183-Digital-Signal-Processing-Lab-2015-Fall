########################################################
# the parser (syntax analyser, evaluates during parse)
########################################################

UndefinedError = 'UndefinedError'
from scanner import Scanner, LexicalError, SyntaxError 

class Parser:
    def __init__(self, text=''):
        self.lex  = Scanner(text)              # embed a scanner
        self.vars = {'pi':3.14159}             # add a variable

    def parse(self, *text):
        if text:                               # main entry-point
            self.lex.newtext(text[0])          # reuse this parser?
        try:
            self.lex.scan()                    # get first token
            self.Goal()                        # parse a sentence
        except SyntaxError:
            print 'Syntax Error at column:', self.lex.start
            self.lex.showerror()
        except LexicalError:
            print 'Lexical Error at column:', self.lex.start
            self.lex.showerror()
        except UndefinedError, name:
            print "'%s' is undefined at column:" % name, self.lex.start
            self.lex.showerror()

    def Goal(self):
        if self.lex.token in ['num', 'var', '(']:
            val = self.Expr()
            self.lex.match('\0')                    # expression?
            print val
        elif self.lex.token == 'set':               # set command?
            self.Assign()           
            self.lex.match('\0')
        else:
            raise SyntaxError

    def Assign(self):
        self.lex.match('set')
        var = self.lex.match('var')
        val = self.Expr()
        self.vars[var] = val           # assign name in dict

    def Expr(self):
        left = self.Factor()
        while 1:
            if self.lex.token in ['\0', ')']:
                return left
            elif self.lex.token == '+':
                self.lex.scan()
                left = left + self.Factor()
            elif self.lex.token == '-':
                self.lex.scan()
                left = left - self.Factor()
            else:
                raise SyntaxError

    def Factor(self):
        left = self.Term()
        while 1:
            if self.lex.token in ['+', '-', '\0', ')']:
                return left
            elif self.lex.token == '*':
                self.lex.scan()
                left = left * self.Term()
            elif self.lex.token == '/':
                self.lex.scan()
                left = left / self.Term()
            else:
                raise SyntaxError

    def Term(self):
        if self.lex.token == 'num':
            val = self.lex.match('num')               # numbers
            return val
        elif self.lex.token == 'var':
            if self.vars.has_key(self.lex.value):
                val = self.vars[self.lex.value]       # lookup name's value
                self.lex.scan()
                return val
            else:
                raise UndefinedError, self.lex.value
        elif self.lex.token == '(':
            self.lex.scan()
            val = self.Expr()                         # sub-expression
            self.lex.match(')')
            return val
        else:
            raise SyntaxError
                
if __name__ == '__main__':
    import testparser                       # self-test code
    testparser.test(Parser, 'parser1')      # test local Parser
