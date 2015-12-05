#########################################################################
# PyTree: sketch arbitrary tree data structures in a scrolled canvas;
# this version uses tree wrapper classes embedded in the viewer gui 
# to support arbitrary trees (i.e.. composition, not viewer subclassing);
# also adds tree node label click callbacks--run tree specific actions;
# see treeview_subclasses.py for subclass-based alternative structure;
# subclassing limits one tree viewer to one tree type, wrappers do not;
# see treeview_left.py for an alternative way to draw the tree object;
# see and run treeview.py for binary and parse tree wrapper test cases;
#########################################################################

from Tkinter import *
from tkMessageBox import showinfo

Width, Height = 350, 350                    # start canvas size (reset per tree)
Rowsz = 100                                 # pixels per tree row
Colsz = 100                                 # pixels per tree col

###################################
# interface to tree object's nodes
###################################

class TreeWrapper:                          # subclass for a tree type
    def children(self, treenode):
        assert 0, 'children method must be specialized for tree type'
    def label(self, treenode):
        assert 0, 'label method must be specialized for tree type'
    def value(self, treenode):
        return ''
    def onClick(self, treenode):            # node label click callback
        return ''
    def onInputLine(self, line, viewer):    # input line sent callback
        pass

##################################
# tree view gui, tree independent
##################################

class TreeViewer(Frame):
    def __init__(self, wrapper, parent=None, tree=None, bg='brown', fg='beige'):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.makeWidgets(bg)                    # build gui: scrolled canvas
        self.master.title('PyTree 1.0')         # assume I'm run standalone
        self.wrapper = wrapper                  # embed a TreeWrapper object
        self.fg = fg                            # setTreeType changes wrapper 
        if tree:
           self.drawTree(tree)

    def makeWidgets(self, bg):
        self.title = Label(self, text='PyTree 1.0')
        self.canvas = Canvas(self, bg=bg, borderwidth=0)
        vbar = Scrollbar(self)
        hbar = Scrollbar(self, orient='horizontal')

        self.title.pack(side=TOP, fill=X)
        vbar.pack(side=RIGHT,  fill=Y)                  # pack canvas after bars
        hbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=TOP, fill=BOTH, expand=YES)

        vbar.config(command=self.canvas.yview)          # call on scroll move
        hbar.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=vbar.set)     # call on canvas move
        self.canvas.config(xscrollcommand=hbar.set)
        self.canvas.config(height=Height, width=Width)  # viewable area size

    def clearTree(self):
        mylabel = 'PyTree 1.0 - ' + self.wrapper.__class__.__name__
        self.title.config(text=mylabel)
        self.unbind_all('<Button-1>')
        self.canvas.delete('all')                       # clear events, drawing

    def drawTree(self, tree):
        self.clearTree()
        wrapper = self.wrapper
        levels, maxrow = self.planLevels(tree, wrapper)
        self.canvas.config(scrollregion=(                     # scrollable area
            0, 0, (Colsz * maxrow), (Rowsz * len(levels)) ))  # upleft, lowright
        self.drawLevels(levels, maxrow, wrapper)

    def planLevels(self, root, wrap):
        levels = []
        maxrow = 0                                       # traverse tree to 
        currlevel = [(root, None)]                       # layout rows, cols
        while currlevel:
            levels.append(currlevel)
            size = len(currlevel)
            if size > maxrow: maxrow = size
            nextlevel = []
            for (node, parent) in currlevel:
                if node != None:
                    children = wrap.children(node)             # list of nodes
                    if not children:
                        nextlevel.append((None, None))         # leave a hole
                    else:
                        for child in children:
                            nextlevel.append((child, node))    # parent link
            currlevel = nextlevel
        return levels, maxrow

    def drawLevels(self, levels, maxrow, wrap):
        rowpos = 0                                         # draw tree per plan
        for level in levels:                               # set click handlers
            colinc = (maxrow * Colsz) / (len(level) + 1)   # levels is treenodes
            colpos = 0
            for (node, parent) in level:
                colpos = colpos + colinc
                if node != None:
                    text = wrap.label(node)
                    more = wrap.value(node)
                    if more: text = text + '=' + more
                    win = Label(self.canvas, text=text, 
                                             bg=self.fg, bd=3, relief=RAISED)
                    win.pack()
                    win.bind('<Button-1>', 
                        lambda e, n=node, handler=self.onClick: handler(e, n))
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

    def onClick(self, event, node):
        label = event.widget
        wrap  = self.wrapper
        text  = 'Label = ' + wrap.label(node)       # on label click
        value = wrap.value(node)
        if value: 
            text = text + '\nValue = ' + value      # add tree text if any
        result = wrap.onClick(node)                 # run tree action if any
        if result:
            text = text + '\n' + result             # add action result
        showinfo('PyTree', text)                    # popup std dialog

    def onInputLine(self, line):                    # feed text to tree wrapper
        self.wrapper.onInputLine(line, self)        # ex: parse and redraw tree

    def setTreeType(self, newTreeWrapper):          # change tree type drawn
        if self.wrapper != newTreeWrapper:          # effective on next draw
            self.wrapper = newTreeWrapper
            self.clearTree()                        # else old node, new wrapper
