# PyTree launcher script
# wrappers for viewing tree types in the book, plus test cases/gui

import string
from Tkinter import *
from treeview_wrappers import TreeWrapper, TreeViewer
from PP2E.Dstruct.Classics import btree
from PP2E.Lang.Parser import parser2

###################################################################
# binary tree wrapper
###################################################################

class BinaryTreeWrapper(TreeWrapper):          # embed binary tree in viewer
    def children(self, node):                  # adds viewer protocols
        try:                                   # to interface with tree
            return [node.left, node.right]
        except: 
            return None
    def label(self, node):
        try:    
            return str(node.data)
        except: 
            return str(node)
    def onInputLine(self, line, viewer):       # on test entry at bottom
        items = string.split(line)             # make tree from text input
        t = btree.BinaryTree()                 # draw resulting btree
        for x in items: t.insert(x)            # no onClick handler here
        viewer.drawTree(t.tree)

###################################################################
# binary tree extension
###################################################################

class BinaryTree(btree.BinaryTree):
    def __init__(self, viewer):                # embed viewer in tree
        btree.BinaryTree.__init__(self)        # but viewer has a wrapper
        self.viewer  = viewer
    def view(self):
        self.viewer.drawTree(self.tree)

###################################################################
# parse tree wrapper
###################################################################

class ParseTreeWrapper(TreeWrapper):
    def __init__(self):                        # embed parse tree in viewer
        self.dict = {}                         # adds viewer protocols
    def children(self, node):
        try:
            return [node.left, node.right]
        except:
            try:
                return [node.var, node.val]
            except: 
                return None
    def label(self, node):
        for attr in ['label', 'num', 'name']:
            if hasattr(node, attr):
                return str(getattr(node, attr))
        return 'set'
    def onClick(self, node):                        # on tree label click
        try:                                        # tree-specific action
            result = node.apply(self.dict)          # evaluate subtree
            return 'Value = ' + str(result)         # show result in popup
        except:
            return 'Value = <error>'
    def onInputLine(self, line, viewer):            # on input line
        p = parser2.Parser()                        # parse expr text
        p.lex.newtext(line)                         # draw resulting tree
        t = p.analyse()
        if t: viewer.drawTree(t)

###################################################################
# canned test cases (or type new nodelists/exprs in input field)
###################################################################

def shownodes(sequence):
    sequence = map(str, sequence)           # convert nodes to strings
    entry.delete(0, END)                    # show nodes in text field
    entry.insert(0, string.join(sequence, ' '))

def test1_binary():                         # tree type is binary wrapper
    nodes = [3, 1, 9, 2, 7]                 # make a binary tree
    tree  = BinaryTree(viewer)              # embed viewer in tree
    for i in nodes: tree.insert(i)            
    shownodes(nodes)                        # show nodes in input field
    tree.view()                             # sketch tree via embedded viewer

def test2_binary():
    nodes = 'badce'
    tree  = btree.BinaryTree()              # embed wrapper in viewer
    for c in nodes: tree.insert(c)          # make a binary tree
    shownodes(nodes)
    viewer.drawTree(tree.tree)              # ask viewer to draw it

def test3_binary():
    nodes = 'abcde'
    tree  = BinaryTree(viewer)
    for c in nodes: tree.insert(c)
    shownodes(nodes)
    tree.view()

def test4_binary():
    tree = BinaryTree(viewer)
    import random                           # make a big binary tree
    nodes = range(100)                      # insert 100 nodes at random
    order = []                              # and sketch in viewer
    while nodes:
        item = random.choice(nodes)
        nodes.remove(item)
        tree.insert(item)
        order.append(item)
    shownodes(order)
    tree.view()

def test_parser(expr):
    parser = parser2.Parser()               # tree type is parser wrapper
    parser.lex.newtext(expr)                # subtrees evaluate when clicked
    tree   = parser.analyse()               # input line parses new expr
    entry.delete(0, END)                    # vars set in wrapper dictionary
    entry.insert(0, expr)                   # see lang/text chapter for parser
    if tree: viewer.drawTree(tree)

def test1_parser(): test_parser("1 + 3 * (2 * 3 + 4)")    
def test2_parser(): test_parser("set temp 1 + 3 * 2 * 3 + 4")
def test3_parser(): test_parser("set result temp + ((1 + 3) * 2) * (3 + 4)")

###################################################################
# build viewer with extra widgets to test tree types
###################################################################

if __name__ == '__main__':
    root = Tk()                             # build a single viewer gui
    bwrapper = BinaryTreeWrapper()          # add extras: input line, test btns
    pwrapper = ParseTreeWrapper()           # make wrapper objects
    viewer   = TreeViewer(bwrapper, root)   # start out in binary mode

    def onRadio():
        if var.get() == 'btree':
            viewer.setTreeType(bwrapper)             # change viewer's wrapper
            for btn in p_btns: btn.pack_forget()     # erase parser test buttons
            for btn in b_btns: btn.pack(side=LEFT)   # unhide binary buttons
        elif var.get() == 'ptree':
            viewer.setTreeType(pwrapper)
            for btn in b_btns: btn.pack_forget()
            for btn in p_btns: btn.pack(side=LEFT)

    var = StringVar()
    var.set('btree')
    Radiobutton(root, text='Binary', command=onRadio, 
                      variable=var, value='btree').pack(side=LEFT)
    Radiobutton(root, text='Parser', command=onRadio, 
                      variable=var, value='ptree').pack(side=LEFT)
    b_btns = []
    b_btns.append(Button(root, text='test1', command=test1_binary))
    b_btns.append(Button(root, text='test2', command=test2_binary))
    b_btns.append(Button(root, text='test3', command=test3_binary))
    b_btns.append(Button(root, text='test4', command=test4_binary))
    p_btns = []
    p_btns.append(Button(root, text='test1', command=test1_parser))
    p_btns.append(Button(root, text='test2', command=test2_parser))
    p_btns.append(Button(root, text='test3', command=test3_parser))
    onRadio()

    def onInputLine():
        line = entry.get()              # use per current tree wrapper type
        viewer.onInputLine(line)        # type a node list or expression

    Button(root, text='input', command=onInputLine).pack(side=RIGHT)
    entry = Entry(root)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entry.bind('<Return>', lambda event: onInputLine())   # button or enter key
    root.mainloop()                                       # start up the gui
