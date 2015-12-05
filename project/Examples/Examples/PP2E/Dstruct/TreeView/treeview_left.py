# an alternative way to draw the tree--tree roots start towards the
# left instead of being centered above children (run me to see how)

from Tkinter import *
import treeview_subclass
from treeview_subclass import Rowsz, Colsz

class TreeViewer(treeview_subclass.TreeViewer):
    def _drawLevels(self, levels, maxrow):
        rowpos = 0
        for level in levels:
            colpos = 0
            for (node, parent) in level:
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
                            colpos, rowpos, arrow='last')
                    node.__rowpos = rowpos
                    node.__colpos = colpos          # mark node, private attrs
                colpos = colpos + Colsz
            rowpos = rowpos + Rowsz


if __name__ == '__main__':
    from PP2E.Dstruct.Classics import btree

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

    def test1():
        t = BinaryTree(viewer)
        for i in [3, 1, 9, 2, 7]: t.insert(i)
        t.view()  

    def test2():
        t = BinaryTree(viewer)
        for c in 'badce': t.insert(c)
        viewer.drawTree(t.tree)

    def test3():
        t = BinaryTree(viewer)
        for c in 'abcde': t.insert(c)
        t.view()

    root = Tk()
    viewer = BinaryTreeViewer(root)
    Button(root, text='test1', command=test1).pack(side=LEFT)
    Button(root, text='test2', command=test2).pack(side=LEFT)
    Button(root, text='test3', command=test3).pack(side=LEFT)
    root.mainloop()
        
