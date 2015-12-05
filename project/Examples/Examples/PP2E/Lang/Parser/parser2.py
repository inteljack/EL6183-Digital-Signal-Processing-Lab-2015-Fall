TraceDefault   = 0
UndefinedError = "UndefinedError"
from scanner import Scanner, SyntaxError, LexicalError


####################################################
# the interpreter (a smart objects tree)
####################################################

class TreeNode:
    def validate(self, dict):           # default error check
        pass
    def apply(self, dict):              # default evaluator
        pass            
    def trace(self, level):             # default unparser
        print '.'*level + '<empty>'
 
# ROOTS

class BinaryNode(TreeNode):
    def __init__(self, left, right):            # inherited methods
        self.left, self.right = left, right     # left/right branches
    def validate(self, dict):                 
        self.left.validate(dict)                # recurse down branches
        self.right.validate(dict) 
    def trace(self, level):
        print '.'*level + '[' + self.label + ']'
        self.left.trace(level+3)
        self.right.trace(level+3)

class TimesNode(BinaryNode):
    label = '*'
    def apply(self, dict):
        return self.left.apply(dict) * self.right.apply(dict)

class DivideNode(BinaryNode):
    label = '/'
    def apply(self, dict):
        return self.left.apply(dict) / self.right.apply(dict)

class PlusNode(BinaryNode):
    label = '+'
    def apply(self, dict):
        return self.left.apply(dict) + self.right.apply(dict)

class MinusNode(BinaryNode):
    label = '-'
    def apply(self, dict):
        return self.left.apply(dict) - self.right.apply(dict)

# LEAVES

class NumNode(TreeNode):
    def __init__(self, num):
        self.num = num                 # already numeric
    def apply(self, dict):             # use default validate
        return self.num
    def trace(self, level):
        print '.'*level + `self.num`

class VarNode(TreeNode):
    def __init__(self, text, start):
        self.name   = text                    # variable name
        self.column = start                   # column for errors
    def validate(self, dict):
        if not dict.has_key(self.name):
            raise UndefinedError, (self.name, self.column)
    def apply(self, dict):
        return dict[self.name]                # validate before apply
    def assign(self, value, dict):
        dict[self.name] = value               # local extension
    def trace(self, level):
        print '.'*level + self.name

# COMPOSITES

class AssignNode(TreeNode):
    def __init__(self, var, val):
        self.var, self.val = var, val
    def validate(self, dict):
        self.val.validate(dict)               # don't validate var
    def apply(self, dict):
        self.var.assign( self.val.apply(dict), dict )
    def trace(self, level):
        print '.'*level + 'set '
        self.var.trace(level + 3)
        self.val.trace(level + 3)
 

####################################################
# the parser (syntax analyser, tree builder)
####################################################

class Parser:
    def __init__(self, text=''):
        self.lex     = Scanner(text)           # make a scanner
        self.vars    = {'pi':3.14159}          # add constants
        self.traceme = TraceDefault
 
    def parse(self, *text):                    # external interface
        if text: 
            self.lex.newtext(text[0])          # reuse with new text
        tree = self.analyse()                  # parse string
        if tree:
            if self.traceme:                   # dump parse-tree?
                print; tree.trace(0)
            if self.errorCheck(tree):          # check names
                self.interpret(tree)           # evaluate tree

    def analyse(self):
        try:
            self.lex.scan()                    # get first token
            return self.Goal()                 # build a parse-tree
        except SyntaxError:
            print 'Syntax Error at column:', self.lex.start
            self.lex.showerror()
        except LexicalError:
            print 'Lexical Error at column:', self.lex.start
            self.lex.showerror()

    def errorCheck(self, tree):
        try:
            tree.validate(self.vars)           # error checker
            return 'ok'
        except UndefinedError, varinfo:
            print "'%s' is undefined at column: %d" % varinfo
            self.lex.start = varinfo[1]
            self.lex.showerror()               # returns None 

    def interpret(self, tree):
        result = tree.apply(self.vars)         # tree evals itself
        if result != None:                     # ignore 'set' result
            print result 

    def Goal(self):
        if self.lex.token in ['num', 'var', '(']:
            tree = self.Expr()
            self.lex.match('\0')
            return tree
        elif self.lex.token == 'set':
            tree = self.Assign()           
            self.lex.match('\0')
            return tree
        else:
            raise SyntaxError

    def Assign(self):
        self.lex.match('set')
        vartree = VarNode(self.lex.value, self.lex.start)
        self.lex.match('var')
        valtree = self.Expr()
        return AssignNode(vartree, valtree)               # two subtrees

    def Expr(self):
        left = self.Factor()                              # left subtree
        while 1:
            if self.lex.token in ['\0', ')']:
                return left
            elif self.lex.token == '+':
                self.lex.scan()
                left = PlusNode(left, self.Factor())      # add root-node
            elif self.lex.token == '-':
                self.lex.scan()
                left = MinusNode(left, self.Factor())     # grows up/right
            else:
                raise SyntaxError

    def Factor(self):
        left = self.Term()
        while 1:
            if self.lex.token in ['+', '-', '\0', ')']:
                return left
            elif self.lex.token == '*':
                self.lex.scan()
                left = TimesNode(left, self.Term())
            elif self.lex.token == '/':
                self.lex.scan()
                left = DivideNode(left, self.Term())
            else:
                raise SyntaxError

    def Term(self):
        if self.lex.token == 'num':
            leaf = NumNode(self.lex.match('num'))
            return leaf
        elif self.lex.token == 'var':
            leaf = VarNode(self.lex.value, self.lex.start)
            self.lex.scan()
            return leaf
        elif self.lex.token == '(':
            self.lex.scan()
            tree = self.Expr()
            self.lex.match(')')
            return tree
        else:
            raise SyntaxError
                

####################################################
# self-test code: use my parser, parser1's tester
####################################################

if __name__ == '__main__':
    import testparser
    testparser.test(Parser, 'parser2')    #  run with Parser class here
