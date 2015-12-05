import random, sys, time
from Tkinter import *
from tkMessageBox import showinfo, askyesno
from PP2E.Gui.Tools.guimaker import GuiMakerWindowMenu

User, Machine = 'user', 'machine'        # players
X, O, Empty   = 'X', 'O', ' '            # board cell states
Fontsz = 50                              # defaults if no constructor args
Degree = 3                               # default=3 rows/cols=tic-tac-toe
Mode   = 'expert1'                       # default machine move strategy


Debug=1
def trace(*args):
    if Debug:
        for arg in args: print arg,
        print

class State:
    def __init__(self, widget, mark):
        self.widget = widget
        self.mark   = mark


class TicTacToeBase(GuiMakerWindowMenu):                    # a kind of Frame
    def __init__(self, parent=None,                         # with a menu bar
                       fg='black', bg='white', fontsz=Fontsz,
                       goesFirst=User, userMark=X, 
                       degree=Degree):
        self.nextMove    = goesFirst
        self.userMark    = userMark
        self.machineMark = (userMark==X and O) or X 
        self.degree      = degree
        self.record      = {'w':0, 'l':0, 'd':0}
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
        self.cells = {}
        self.board = {}              
        for i in range(self.degree):
            frm = Frame(self)
            frm.pack(expand=YES, fill=BOTH)
            for j in range(self.degree):
                widget = Label(frm, fg=fg, bg=bg, 
                                    text=' ', font=('courier', fontsz, 'bold'),
                                    relief=SUNKEN, bd=4, padx=10, pady=10)
                widget.pack(side=LEFT, expand=YES, fill=BOTH)
                widget.bind('<Button-1>', self.onLeftClick)
                state = State(widget, Empty)
                self.cells[widget] = state
                self.board[(i, j)] = state

    def onLeftClick(self, event):
        cell = event.widget
        if self.nextMove == User and self.cells[cell].mark == Empty:
            self.cells[cell].widget.config(text=self.userMark)
            self.cells[cell].mark = self.userMark
            self.nextMove = Machine
            self.checkFinish()
            self.machineMove()

    def machineMove(self):
        pick = self.pickMove()
        self.board[pick].mark = self.machineMark
        self.board[pick].widget.config(text=self.machineMark)
        self.checkFinish()
        self.nextMove = User      # wait for next left click or quit

    def clearBoard(self):
        for cell in self.board.keys():
            self.board[cell].mark = Empty
            self.board[cell].widget.config(text=' ')

    #
    # end test
    #

    def checkDraw(self, board=None):
        board = board or self.board
        for coord in board.keys():
            if board[coord].mark == Empty: 
                return 0
        return 1  # none empty = draw or win
 
    def checkWin(self, mark, board=None):
        board = board or self.board
        for row in range(self.degree):
            for col in range(self.degree):
                if board[(row, col)].mark != mark:         # check across
                    break                                  # row=all mark?
            else: 
                return 1 
        for col in range(self.degree): 
            for row in range(self.degree):                 # check down
                if board[(row, col)].mark != mark:         # break to next col
                    break
            else: 
                return 1 
        for row in range(self.degree):                     # check diag1
            col = row                                      # row == col
            if board[(row, col)].mark != mark: break 
        else:
            return 1
        for row in range(self.degree):                     # check diag2
            col = (self.degree-1) - row                    # row+col = degree-1
            if board[(row, col)].mark != mark: break
        else:
            return 1

    def checkFinish(self):
        outcome = None
        if self.checkWin(self.userMark):
            outcome = "You've won!"
            self.record['w'] = self.record['w'] + 1
        elif self.checkWin(self.machineMark):
            outcome = 'I win again :-)'
            self.record['l'] = self.record['l'] + 1
        elif self.checkDraw():
            outcome = 'Looks like a draw'
            self.record['d'] = self.record['d'] + 1
        if outcome:
            result = 'Game Over: ' + outcome 
            if not askyesno('PyToe', result + '\n\nPlay another game?'):
                self.onStats()
                self.quit()
                sys.exit()  # don't return to caller
            else:
                self.clearBoard()  
                # return and make move or wait for click
                # player who moved last moves second in next game

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
                 'wins: %(w)d, losses: %(l)d, draws: %(d)d' % self.record)


#
# subclass to customize move selection
#
 
class TicTacToeRandom(TicTacToeBase):
    def pickMove(self):
        empties = []
        for coord in self.board.keys():
            if self.board[coord].mark == Empty:
                empties.append(coord)
        return random.choice(empties)


class TicTacToeSmart(TicTacToeBase):
    def pickMove(self):
        self.update(); time.sleep(2)  # too fast!
        countMarks = self.countAcrossDown(), self.countDiagonal()
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[move].mark == Empty:
                    if self.isWin(move, countMarks):
                        trace('Win', move)
                        return move
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[move].mark == Empty:
                    if self.isBlock(move, countMarks):
                        trace('Block', move)
                        return move
        best = 0
        for row in range(self.degree):
            for col in range(self.degree):
                move = (row, col)
                if self.board[move].mark == Empty:
                    score = self.scoreMove(move, countMarks)
                    if score >= best:
                        pick = move
                        best = score
                    trace('Score', move, score)
        trace('Picked', pick, 'score', best)
        return pick

    def countAcrossDown(self):
        countRows  = {}                        # sparse data structure
        countCols  = {}                        # zero counts aren't added 
        for row in range(self.degree):
            for col in range(self.degree):
                mark = self.board[(row, col)].mark
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
            mark = self.board[(row, col)].mark
            countDiag1[mark] = countDiag1[mark] + 1
        countDiag2 = tally.copy()
        for row in range(self.degree):
            col  = (self.degree-1) - row
            mark = self.board[(row, col)].mark
            countDiag2[mark] = countDiag2[mark] + 1
        return countDiag1, countDiag2

    def isWin(self, move, countMarks): 
        self.board[move].mark = self.machineMark
        isWin = self.checkWin(self.machineMark)
        self.board[move].mark = Empty
        return isWin

    def isBlock(self, move, countMarks): 
        self.board[move].mark = self.userMark
        isLoss = self.checkWin(self.userMark)
        self.board[move].mark = Empty
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
                if self.board[move].mark == Empty:
                    score = self.scoreMove(move, countMarks)
                    if score > best:
                        pick = move
                        best = score
        trace('Picked', pick, 'score', best)
        return pick

    def countAcrossDown(self):
        tally = {'X':0, 'O':0, ' ':0}              # uniform with diagonals
        countRows  = []                            # no entries missing 
        countCols  = []
        for row in range(self.degree):
            countRows.append(tally.copy())
            countCols.append(tally.copy())
        for row in range(self.degree):
            for col in range(self.degree):
                mark = self.board[(row, col)].mark
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


import copy
class TicTacToeMinimax(TicTacToeBase):
    def pickMove(self):
        self.update()
        marks = filter(lambda val: val.mark != Empty, self.board.values())
        if not marks:
            return (self.degree / 2, self.degree / 2)
        else:
            t1 = time.clock()
            maxdepth = len(marks) + 4
            boardCopy = {}
            for key in self.board.keys():
                boardCopy[key] = State(None, self.board[key].mark)
            pick = self.findMax(boardCopy, maxdepth)[1]
            trace('Time to move:', time.clock() - t1)
            return pick

    def checkLeaf(self, board):
        if self.checkWin(self.machineMark, board):  # score from machine's view
            return +1                               # a win is good; a loss bad
        elif self.checkWin(self.userMark, board):
            return -1
        elif self.checkDraw(board):
            return 0
        else:
            return None

    def findMax(self, board, depth):    # machine move level
        if depth == 0:                  # find start of best move sequence
            return 0, None
        else:
            term = self.checkLeaf(board)
            if term != None:                       # depth cutoff 
                return term, None                  # or endgame detected
            else:                                  # or check countermoves
                best = -2
                for move in board.keys():
                    if board[move].mark == Empty:
                        next = copy.deepcopy(board)
                        next[move].mark = self.machineMark
                        below, m = self.findMin(next, depth-1)  
                        if below > best:
                            best = below
                            pick = move
                return best, pick

    def findMin(self, board, depth):    # user move level-find worst case
        if depth == 0:                  # assume she will do her best
            return 0, None
        else:
            term = self.checkLeaf(board)
            if term != None:                       # depth cutoff 
                return term, None                  # or endgame detected
            else:                                  # or check countermoves
                best = +2
                for move in board.keys():
                    if board[move].mark == Empty:
                        next = copy.deepcopy(board)
                        next[move].mark = self.userMark
                        below, m = self.findMax(next, depth-1)  
                        if below < best:
                            best = below
                            pick = move
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
        trace(opts)                                # on cmd line: '-name value'
        apply(TicTacToe, (), opts).mainloop()

