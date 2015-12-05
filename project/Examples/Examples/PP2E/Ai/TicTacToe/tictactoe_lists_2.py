# poss opts:
#    x make board just marks (not State), use board.copy() (not deepcopy)
#    x use arrays for board, indexing (not hash + compare)
#      also speeds draw and checkWin - use 'in' and list.count on entire row
#    - don't board.copy-- just set mark, recure, set Empty  [seems to have no effect]
#    - use scoreMove at cutoff depth
#    x checkFinish should only look for wins at move just made, not all r,c [this]
#      note that could use countMarks method on comments below too, but then 
#      incure cost to calculate counts at each state
# see _lists.py for notes
####################################################################


import random, sys, time
from Tkinter import *
from tkMessageBox import showinfo, askyesno
from PP2E.Gui.Tools.guimaker import GuiMakerWindowMenu

User, Machine = 'user', 'machine'        # players
X, O, Empty   = 'X', 'O', ' '            # board cell states
Fontsz = 50                              # defaults if no constructor args
Degree = 3                               # default=3 rows/cols=tic-tac-toe
Mode   = 'expert2'                       # default machine move strategy

Debug=1
def trace(*args):
    if Debug:
        for arg in args: print arg,
        print

class Record:
    def __init__(self):
        self.win = self.loss = self.draw = 0

class TicTacToeBase(GuiMakerWindowMenu):                    # a kind of Frame
    def __init__(self, parent=None,                         # with a menu bar
                       fg='black', bg='white', fontsz=Fontsz,
                       goesFirst=User, userMark=X, 
                       degree=Degree):
        self.nextMove    = goesFirst
        self.userMark    = userMark
        self.machineMark = (userMark==X and O) or X 
        self.degree      = degree
        self.record      = Record()
        self.makeWidgets = (lambda s=self, f=fg, b=bg, fs=fontsz: 
                                         s.drawBoard(f, b, fs))
        GuiMakerWindowMenu.__init__(self, parent=parent)
        self.master.title('PyToe 1.0')
        if goesFirst == Machine: self.machineMove()   # else wait for click
        
    def start(self):
        self.helpButton = None
        self.toolBar    = None
        self.menuBar    = [ ('File', 0, [('Stats', 0, self.onStats),
                                         ('Quit',  0, self.quit)]),
                            ('Help', 0, [('About', 0, self.onAbout)]) ]

    def drawBoard(self, fg, bg, fontsz):
        self.coord = {}
        self.label = {}
        self.board = []
        for i in range(self.degree):
            self.board.append([0] * self.degree)
            frm = Frame(self)
            frm.pack(expand=YES, fill=BOTH)
            for j in range(self.degree):
                widget = Label(frm, fg=fg, bg=bg, 
                                    text=' ', font=('courier', fontsz, 'bold'),
                                    relief=SUNKEN, bd=4, padx=10, pady=10)
                widget.pack(side=LEFT, expand=YES, fill=BOTH)
                widget.bind('<Button-1>', self.onLeftClick)
                self.coord[widget] = (i, j)
                self.label[(i, j)] = widget
                self.board[i][j]   = Empty

    def onLeftClick(self, event):
        label    = event.widget
        row, col = self.coord[label]
        if self.nextMove == User and self.board[row][col] == Empty:
            label.config(text=self.userMark)
            self.board[row][col] = self.userMark
            self.nextMove = Machine
            self.checkFinish(row, col)
            self.machineMove()

    def machineMove(self):
        row, col = self.pickMove()
        self.board[row][col] = self.machineMark
        label = self.label[(row, col)]
        label.config(text=self.machineMark)
        self.checkFinish(row, col)
        self.nextMove = User      # wait for next left click or quit

    def clearBoard(self):
         for row, col in self.label.keys():
            self.label[(row, col)].config(text=' ')
            self.board[row][col] = Empty

    #
    # end test
    #

    def checkDraw(self, board=None):
        board = board or self.board
        for row in board:
            if Empty in row:  
                return 0
        return 1  # none empty = draw or win
 
    def checkWin(self, mark, row, col, board=None):
        board = board or self.board
        if board[row].count(mark) == self.degree:          # check across
            return 1
        for row in board:                                  # check down
            if row[col] != mark: break
        else:
            return 1 
        if row == col:                                     # check diag1
            col = 0
            for row in board:
                if row[col] != mark: break
                col = col+1
            else:
                return 1
        if row+col == self.degree-1:                       # check diag2
            col = self.degree-1
            for row in board:
                if row[col] != mark: break
                col = col-1
            else:
                return 1
        return 0

    def checkFinish(self, row, col):
        outcome = None
        if self.checkWin(self.userMark, row, col):
            outcome = "You've won!"
            self.record.win = self.record.win + 1
        elif self.checkWin(self.machineMark, row, col):
            outcome = 'I win again :-)'
            self.record.loss = self.record.loss + 1
        elif self.checkDraw():
            outcome = 'Looks like a draw'
            self.record.draw = self.record.draw + 1
        if outcome:
            result = 'Game Over: ' + outcome 
            if not askyesno('PyToe', result + '\n\nPlay another game?'):
                self.onStats()
                self.quit()
                sys.exit()          # don't return to caller
            else:
                self.clearBoard()   # return and make move or wait for click
                                    # player who moved last moves second next
    def onAbout(self):
        showinfo('PyToe 1.0', 'PyToe 1.0\n'
                              'July, 1999\n'
                              'A Tic-tac-toe board game\n'
                              'Programming Python 2E\n'
                              '\nCommand-line args:\n'
                              '-degree controls board size\n'
                              '-mode controls machine skill\n'
                              '-fg -bg -fontsz control board\n'
                              'plus: -goesFirst, -userMark')
    def onStats(self):
        showinfo('PyToe Stats',
                 'Your results:\n'
                 'wins: %(win)d,  losses: %(loss)d,  draws: %(draw)d'
                  % self.record.__dict__)


#
# subclass to customize move selection
#

class TicTacToeRandom(TicTacToeBase):
    def pickMove(self):
        empties = []
        for row in self.degree:
            for col in self.degree:
                if self.board[row][col] == Empty:
                    empties.append((row, col))
        return random.choice(empties)


class TicTacToeSmart(TicTacToeBase):
    def pickMove(self):
        self.update(); time.sleep(2)  # too fast!
        countMarks = self.countAcrossDown(), self.countDiagonal()
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[row][col] == Empty:
                    if self.isWin(move, countMarks):
                        return move
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[row][col] == Empty:
                    if self.isBlock(move, countMarks):
                        return move
        best = 0
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[row][col] == Empty:
                    score = self.scoreMove(move, countMarks)
                    if score >= best:
                        pick = move
                        best = score
        trace('Picked', pick, 'score', best)
        return pick

    def countAcrossDown(self):
        countRows  = {}                        # sparse data structure
        countCols  = {}                        # zero counts aren't added 
        for row in range(self.degree):
            for col in range(self.degree):
                mark = self.board[row][col]
                try:
                    countRows[(row, mark)] = countRows[(row, mark)] + 1
                except KeyError:
                    countRows[(row, mark)] = 1
                try: 
                    countCols[(col, mark)] = countCols[(col, mark)] + 1
                except KeyError:
                    countCols[(col, mark)] = 1
        return countRows, countCols

    def countDiagonal(self):
        tally = {'X':0, 'O':0, ' ':0}
        countDiag1 = tally.copy()
        for row in range(self.degree): 
            col  = row
            mark = self.board[row][col]
            countDiag1[mark] = countDiag1[mark] + 1
        countDiag2 = tally.copy()
        for row in range(self.degree):
            col  = (self.degree-1) - row
            mark = self.board[row][col]
            countDiag2[mark] = countDiag2[mark] + 1
        return countDiag1, countDiag2

    def isWin(self, (row, col), countMarks): 
        self.board[row][col] = self.machineMark
        isWin = self.checkWin(self.machineMark, row, col)
        self.board[row][col] = Empty
        return isWin

    def isBlock(self, (row, col), countMarks): 
        self.board[row][col] = self.userMark
        isLoss = self.checkWin(self.userMark, row, col)
        self.board[row][col] = Empty
        return isLoss

    def scoreMove(self, (row, col), 
                 ((countRows, countCols), (countDiag1, countDiag2)) ):
        return (
           countCols.get((col, self.machineMark), 0) * 11 +
           countRows.get((row, self.machineMark), 0) * 11 + 
           countDiag1[self.machineMark] * 11 + 
           countDiag1[self.machineMark] * 11 
           +
           countCols.get((col, self.userMark), 0) * 10 +
           countRows.get((row, self.userMark), 0) * 10 + 
           countDiag1[self.userMark] * 10 + 
           countDiag1[self.userMark] * 10 
           +
           countCols.get((col, Empty), 0) * 11 +
           countRows.get((row, Empty), 0) * 11 + 
           countDiag1[Empty] * 11 + 
           countDiag1[Empty] * 11)


class TicTacToeExpert1(TicTacToeSmart):
    def pickMove(self):
        self.update(); time.sleep(2)
        countMarks = self.countAcrossDown(), self.countDiagonal()
        best = 0
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[row][col] == Empty:
                    score = self.scoreMove(move, countMarks)
                    if score > best:
                        pick = move
                        best = score
        trace('Picked', pick, 'score', best)
        return pick

    def countAcrossDown(self):
        tally = {'X':0, 'O':0, ' ':0}              # uniform with diagonals
        countRows  = []                            # no entries missing 
        countCols  = []                            # tally * degree fails
        for row in range(self.degree):
            countRows.append(tally.copy())
            countCols.append(tally.copy())
        for row in range(self.degree):
            for col in range(self.degree):
                mark = self.board[row][col]
                countRows[row][mark] = countRows[row][mark] + 1
                countCols[col][mark] = countCols[col][mark] + 1
        return countRows, countCols
        
    def scoreMove(self, (row, col), 
                 ((countRows, countCols), (countDiag1, countDiag2)) ):
        score  = 0
        mine   = self.machineMark  
        user   = self.userMark    
                                                      # for empty slot (r,c):
        partof = [countRows[row], countCols[col]]     # check move row and col
        if row == col:                                # plus diagonals, if any
            partof.append(countDiag1)
        if row+col == self.degree-1: 
            partof.append(countDiag2)

        for line in partof:                                     
            if line[mine] == self.degree-1 and line[Empty] == 1:
                score = score + 51                            # 1 move to win
        for line in partof:
            if line[user] == self.degree-1 and line[Empty] == 1: 
                score = score + 25                            # 1 move to loss
        for line in partof:
            if line[mine] == self.degree-2 and line[Empty] == 2: 
                score = score + 10                            # 2 moves to win
        for line in partof:
            if line[user] == self.degree-2 and line[Empty] == 2:
                score = score + 8                             # 2 moves to loss
        for line in partof:
            if line[Empty] == self.degree:                    # prefer openness
                score = score + 1

        if score:
            return score                         # detected pattern here?
        else:                                    # else use weighted scoring
            for line in partof:
                score = score + line[mine] * 3 + line[user] + line[Empty] * 2
            return score / float(self.degree)


class TicTacToeExpert2(TicTacToeExpert1):
    def scoreMove(self, (row, col), 
                 ((countRows, countCols), (countDiag1, countDiag2)) ):
        score  = 0
        mine   = self.machineMark  
        user   = self.userMark    
                                                      # for empty slot (r,c):
        partof = [countRows[row], countCols[col]]     # check move row and col
        if row == col:                                # plus diagonals, if any
            partof.append(countDiag1)
        if row+col == self.degree-1: 
            partof.append(countDiag2)

        weight = 3L ** (self.degree * 2)
        for  ahead in range(1, self.degree):
            for line in partof: 
                if line[mine] == self.degree-ahead and line[Empty] == ahead: 
                    score = score + weight

                if line[user] == self.degree-ahead and line[Empty] == ahead: 
                    score = score + weight / 3
            weight = weight / 9

        if score:
            return score                         # detected pattern here?
        else:                                    # else use weighted scoring
            for line in partof:
                score = score + line[mine] * 3 + line[user] + line[Empty] * 2
            return score / float(self.degree)


class TicTacToeMinimax(TicTacToeBase):
    def pickMove(self):
        self.update()
        numMarks = self.degree ** 2
        for row in self.board:
            numMarks = numMarks - row.count(Empty)
        if numMarks == 0:
            return (self.degree / 2, self.degree / 2)
        else:
            t1 = time.clock()
            maxdepth = numMarks + 4
            pick = self.findMax(self.board, maxdepth)[1]
            print 'Time to move:', time.clock() - t1
            return pick

    def checkLeaf(self, board):                                # machine view
        ??? only need to look for moving player's win
        ??? same in general case for checkFinish
        if self.checkWin(self.machineMark, row, col, board):  
            return +1                                          # a win is good
        elif self.checkWin(self.userMark, row, col, board):
            return -1                                          # a loss is bad
        elif self.checkDraw(board):
            return 0                                           # ignore draws
        else:
            return None

    def findMax(self, board, depth):        # machine move level
        if depth == 0:                      # find start of best move sequence
            return 0, None                  # could return static score here???
        else:
            term = self.checkLeaf(board???)
            if term != None:                       # depth cutoff 
                return term, None                  # or endgame detected
            else:                                  # or check countermoves
                best = -2
                for row in range(self.degree):
                    for col in range(self.degree):
                        if board[row][col] == Empty:
                            board[row][col] = self.machineMark
                            below, m = self.findMin(board, depth-1)
                            board[row][col] = Empty  
                            if below > best:
                                best = below
                                pick = (row, col)
                return best, pick

    def findMin(self, board, depth):        # user move level-find worst case
        if depth == 0:                      # assume she will do her best
            return 0, None
        else:
            term = self.checkLeaf(board???)
            if term != None:                       # depth cutoff 
                return term, None                  # or endgame detected
            else:                                  # or check countermoves
                best = +2
                for row in range(self.degree):
                    for col in range(self.degree):
                        if board[row][col] == Empty:
                            board[row][col] = self.userMark
                            below, m = self.findMax(board, depth-1)  
                            board[row][col] = Empty
                            if below < best:
                                best = below
                                pick = (row, col)
                return best, pick


#
# game object generator - external interface 
#

def TicTacToe(mode=Mode, **args):
    if mode == 'random':
        return apply(TicTacToeRandom,  (), args)
    if mode == 'smart':
        return apply(TicTacToeSmart, (), args)
    if mode == 'expert1':
        return apply(TicTacToeExpert1, (), args)
    if mode == 'expert2':
        return apply(TicTacToeExpert2, (), args)
    if mode == 'minimax':
        return apply(TicTacToeMinimax, (), args)
    assert 0, 'Bad mode argument'


#
# command-line logic
#

if __name__ == '__main__': 
    if len(sys.argv) == 1:
        TicTacToe().mainloop()   # default=3-across
    else:
        # ex: TicTacToe.py -degree 5 -mode smart -bg blue -fg white -fontsz 30
        needEval = ['-degree']
        args = sys.argv[1:]
        opts = {} 
        for i in range(0, len(args), +2):
            if args[i] in needEval:
                opts[args[i][1:]] = eval(args[i+1])
            else:
                opts[args[i][1:]] = args[i+1]      # any constructor arg
        print opts                                 # on cmd line: '-name value'
        apply(TicTacToe, (), opts).mainloop()

