#######################################################################
# PyTree: sketch arbitrary tree data structures in a scrolled canvas;
# this version uses viewer gui subclassing to support arbitrary trees;
#######################################################################

from Tkinter import *
Width, Height = 350, 350
Rowsz = 100
Colsz = 100

class TreeViewer(Frame):
    def __init__(self, parent=None, tree=None, bg='brown', fg='grey'):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self._makeWidgets(bg)
        self.master.title('PyTree 1.0')
        self.fg = fg
        if tree:
           self.drawTree(tree)

    def _makeWidgets(self, bg):
        title = Label(self, text='PyTree 1.0 - ' + self._type())
        self.canvas = Canvas(self, bg=bg, borderwidth=0)
        vbar = Scrollbar(self)
        hbar = Scrollbar(self, orient='horizontal')

        title.pack(side=TOP, fill=X)
        vbar.pack(side=RIGHT,  fill=Y)                  # pack canvas after bars
        hbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        vbar.config(command=self.canvas.yview)          # call on scroll move
        hbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=vbar.set)     # call on canvas move
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.config(height=Height, width=Width)  # viewable area size

    def drawTree(self, tree):                           # clients call this
        self.canvas.delete('all')
        levels, maxrow = self._planLevels(tree)
        self.canvas.config(scrollregion=(               # scrollable area size
                           0, 0,                        # upperleft, lowerright
                           (Colsz * maxrow), (Rowsz * len(levels)) ))
        self._drawLevels(levels, maxrow)

    def _planLevels(self, root):
        levels = []
        maxrow = 0
        currlevel = [(root, None)]
        while currlevel:
            levels.append(currlevel)
            size = len(currlevel)
            if size > maxrow: maxrow = size
            nextlevel = []
            for (node, parent) in currlevel:
                if node != None:
                    children = self._children(node)            # list of nodes
                    if not children:
                        nextlevel.append((None, None))         # leave a hole
                    else:
                        for child in children:
                            nextlevel.append((child, node))    # parent link
            currlevel = nextlevel
        return levels, maxrow

    def _drawLevels(self, levels, maxrow):
        rowpos = 0
        for level in levels:
            colinc = (maxrow * Colsz) / (len(level) + 1)
            colpos = 0
            for (node, parent) in level:
                colpos = colpos + colinc
                if node != None:
                    text = self._label(node)
                    if self._value(node): text = text + '=' + self._value(node)
                    win = Label(self.canvas, text=text, 
                                             bg=self.fg, bd=3, relief=RAISED)
                    win.pack()
                    self.canvas.create_window(colpos, rowpos, anchor=NW, 
                                window=win, width=Colsz*.5, height=Rowsz*.5)
                    if parent != None:
                        self.canvas.create_line(
                            parent.__colpos + Colsz*.25,    # from x-y, to x-y
                            parent.__rowpos + Rowsz*.5,
                            colpos + Colsz*.25, rowpos, arrow='last', width=1)
                    node.__rowpos = rowpos
                    node.__colpos = colpos          # mark node, private attrs
            rowpos = rowpos + Rowsz

    def _type(self):
        return self.__class__.__name__
    def _children(self, node):
        assert 0, '_children method must be specialized for tree type'
    def _label(self, node):
        assert 0, '_label method must be specialized for tree type'
    def _value(self, node):
        return None # specialize me for trees with key->value type nodes

if __name__ == '__main__': 
    from PP2E.Dstruct.Classics import btree               # import btree
    class BinaryTree(btree.BinaryTree):
        def __init__(self, viewer):
            btree.BinaryTree.__init__(self)
            self.viewer = viewer
        def view(self): 
            self.viewer.drawTree(self.tree)

    class BinaryTreeViewer(TreeViewer):
        def _children(self, node):
            try:    
                return [node.left, node.right]
            except: 
                return None
        def _label(self, node):
            try:    
                return str(node.data)
            except: 
                return str(node)

    from PP2E.Lang.Parser import parser2                  # import parser2
    class ParseTreeViewer(TreeViewer):
        def _children(self, node):
            try:
                return [node.left, node.right]
            except:
                try:
                    return [node.var, node.val]
                except: 
                    return None
        def _label(self, node):
            for attr in ['label', 'num', 'name']:
                if hasattr(node, attr):
                    return str(getattr(node, attr))
            return 'set'

    def test1():
        t = BinaryTree(bviewer)
        for i in [3, 1, 9, 2, 7]: t.insert(i)
        t.view()  

    def test2():
        t = btree.BinaryTree()
        for c in 'badce': t.insert(c)
        bviewer.drawTree(t.tree)

    def test3():
        t = BinaryTree(bviewer)
        for c in 'abcde': t.insert(c)
        t.view()

    def test4():
        p = parser2.Parser()
        p.lex.newtext("1 + 3 * (2 * 3 + 4)")
        t = p.analyse()
        if t: pviewer.drawTree(t)

    def test5():
        p = parser2.Parser()
        p.lex.newtext("set temp 1 + 3 * 2 * 3 + 4")
        t = p.analyse()
        if t: pviewer.drawTree(t)

    def test6():
        p = parser2.Parser()
        p.lex.newtext("set result temp + ((1 + 3) * 2) * (3 + 4)")
        t = p.analyse()
        if t: pviewer.drawTree(t)

    root = Tk()
    bviewer = BinaryTreeViewer(Toplevel())
    Button(root, text='test1', command=test1).pack(side=LEFT)
    Button(root, text='test2', command=test2).pack(side=LEFT)
    Button(root, text='test3', command=test3).pack(side=LEFT)

    pviewer = ParseTreeViewer(Toplevel())
    Button(root, text='test4', command=test4).pack(side=LEFT)
    Button(root, text='test5', command=test5).pack(side=LEFT)
    Button(root, text='test6', command=test6).pack(side=LEFT)
    root.mainloop()
