import random, sys
from Tkinter import *
from tkMessageBox import showinfo, askyesno
from PP2E.Gui.Tools.guimaker import GuiMakerWindowMenu

User, Machine = 1, 2             # players
X, O, Empty   = 'X', 'O', ' '    # board cell states
Dumb, Smart   = 1, 2             # random or heuristic machine play
Degree = 3                       # default=3 rows/cols=tic-tac-toe
Mode   = Smart                   # how the machine makes moves

Debug=1
def trace(*args):
    if Debug:
        for arg in args: print arg,
        print

class State:
    def __init__(self, widget, mark):
        self.widget = widget
        self.mark   = mark

class TicTacToe(GuiMakerWindowMenu):                        # a kind of Frame
    def __init__(self, parent=None,                         # with a menu bar
                       fg='black', bg='white', 
                       goesFirst=User, userIsX=1, mode=Mode, degree=Degree):
        self.nextMove    = goesFirst
        self.userMark    = [O, X][userIsX]
        self.machineMark = (userIsX and O) or X  
        self.machineMode = mode
        self.degree      = degree
        self.makeWidgets = lambda s=self, f=fg, b=bg: s.drawBoard(f, b)
        GuiMakerWindowMenu.__init__(self, parent, grid=1)
        self.master.title('PyToe 1.0')
        self.play()
        
    def start(self):
        self.helpButton = None
        self.toolBar    = None
        self.menuBar    = [ ('File', 0, [('Stats', 0, self.onStats),
                                         ('Quit',  0, self.quit)]),
                            ('Help', 0, [('About', 0, self.onAbout)]) ]

    def drawBoard(self, fg, bg):
        self.cells = {}
        self.board = {}              
        for i in range(self.degree):
            for j in range(self.degree):
                widget = Label(self, fg=fg, bg=bg, 
                                     text=' ', font=('courier', 50, 'bold'),
                                     relief=SUNKEN, bd=4, padx=20, pady=20)
                widget.grid(row=i, column=j, sticky=NSEW)
                widget.bind('<Button-1>', self.onLeftClick)
                state = State(widget, Empty)
                self.cells[widget] = state
                self.board[(i, j)] = state
        for i in range(self.degree):
            self.rowconfigure(i, weight=1) 
            self.columnconfigure(i, weight=1)     # resizable

    def play(self):
        self.record = {'w':0, 'l':0, 'd':0}
        self.userPick = IntVar()
        while 1:
            if self.nextMove == Machine:
                self.machineMove()
                self.nextMove = User
            else:
                self.wait_variable(self.userPick)
                self.nextMove = Machine
            outcome = self.checkFinish()
            if outcome:
                result = 'Game Over: ' + outcome 
                if askyesno('PyToe', result + '\n\nPlay Again?'):
                    self.clearBoard()
                else:
                    break   
        self.onStats()

    def onLeftClick(self, event):
        cell = event.widget
        if self.nextMove == User and self.cells[cell].mark == Empty:
            self.cells[cell].widget.config(text=self.userMark)
            self.cells[cell].mark = self.userMark
            self.update()
            self.userPick.set(self.userPick.get() + 1)

    def machineMove(self):
        pick = self.pickMove()
        self.board[pick].mark = self.machineMark
        self.board[pick].widget.config(text=self.machineMark)

    def clearBoard(self):
        for cell in self.board.keys():
            self.board[cell].mark = Empty
            self.board[cell].widget.config(text=' ')

    #
    # end test
    #

    def checkDraw(self):
        for coord in self.board.keys():
            if self.board[coord].mark == Empty: 
                return 0
        return 1  # none empty = draw or win
 
    def checkWin(self, mark):
        for row in range(self.degree):
            for col in range(self.degree):
                if self.board[(row, col)].mark != mark: 
                    break                                  # check across
            else:                                          # row=all mark?
                return 1 
        for col in range(self.degree): 
            for row in range(self.degree):                 # check down
                if self.board[(row, col)].mark != mark:    # break to next col
                    break
            else: 
                return 1 
        for row in range(self.degree):                     # check diag1
            if self.board[(row, row)].mark != mark: break  # row == col
        else:
            return 1
        for row in range(self.degree):                     # check diag2
            col = (self.degree-1) - row                    # col = degree-row-1
            if self.board[(row, col)].mark != mark: break
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
        return outcome

    #
    # move selection
    #

    def countAcrossDown(self):
        countRows  = {}
        for row in range(self.degree):
            for col in range(self.degree):
                mark = self.board[(row, col)].mark
                try:
                    countRows[(row, mark)] = countRows[(row, mark)] + 1
                except KeyError:
                    countRows[(row, mark)] = 1
        countCols  = {}
        for col in range(self.degree):
            for row in range(self.degree):
                mark = self.board[(row, col)].mark
                try: 
                    countCols[(col, mark)] = countCols[(col, mark)] + 1
                except KeyError:
                    countCols[(col, mark)] = 1
        return countRows, countCols

    def countDiagonal(self):
        tally = {'X':0, 'O':0, ' ':0}
        countDiag1 = tally.copy()
        for row in range(self.degree): 
            for col in range(self.degree):
                if row == col:
                    mark = self.board[(row, col)].mark
                    countDiag1[mark] = countDiag1[mark] + 1
        countDiag2 = tally.copy()
        for row in range(self.degree):
            for col in range(self.degree):
                if row+col == self.degree-1:
                    mark = self.board[(row, col)].mark
                    countDiag2[mark] = countDiag2[mark] + 1
        return countDiag1, countDiag2
                
    def isWinFor(self, playerMark, 
                 (row, col), 
                 ((countRows, countCols), (countDiag1, countDiag2)) ):
        return (
            (countCols[col, self.machineMark] == self.degree-1)
            or
            (countRows[row, self.machineMark] == self.degree-1)
            or
            (row == col and 
             countDiag1[self.machineMark] == self.degree-1)
            or
            (row + col == self.degree-1 and 
             countDiag2[self.machineMark] == self.degree-1) )

    def isWin(self, move, countMarks): 
        return self.isWinFor(self.machineMark, move, countMarks)
    def isBlock(self, move, countMarks): 
        return self.isWinFor(self.userMark, move, countMarks)

    def scoreMove(self, (row, col), 
                 ((countRows, countCols), (countDiag1, countDiag2)) ):
        score = 0
        if (countCols[col, self.machineMark] >= 1 and
            countCols[col][Empty] >= 1):
            score = score + 10
        if (countRows[row, self.machineMark] >= 1 and
            countRows[row][Empty] >= 1):
            score = score + 10
        # ??? +diags
                         
        #??? or: number X's in col * 25, number O's * 10,...
        #??? diags: could just add non-diag cells with 0 values
        return score
        
    def pickMove(self):
        if self.machineMode == Dumb:
            empties = []
            for coord in self.board.keys():
                if self.board[coord].mark == Empty:
                    empties.append(coord)
            return random.choice(empties)
        else:
            self.config(cursor='watch')
            best = 0
            countMarks = self.countAcrossDown(), self.countDiagonal()
            for row in range(self.degree):
                for col in range(self.degree):
                    move = (row, col)
                    if self.board[move].mark == Empty:
                        if self.isWin(move, countMarks):
                            return move
                        elif self.isBlock(move, countmarks):
                            return move
                        else:
                            score = self.scoreMove(move, countMarks)
                            if score >= best:
                                pick = move
                                best = score
                            trace('Score', move, score)
            trace('Picked', pick, 'score', best)
            self.config(cursor='arrow')
            return pick

    def onAbout(self):
        showinfo('PyToe 1.0', 'PyToe 1.0\n'
                              'July, 1999\n'
                              'A Tic-tac-toe Board Game\n'
                              'Degree controls board size\n'
                              'Programming Python 2E')
    def onStats(self):
        showinfo('Your results:\n'
                 'wins: %(w)d, losses: %(l)d, draws: %(d)d' % self.record)

if __name__ == '__main__': 
    if len(sys.argv) == 1:
        TicTacToe().mainloop()
    else:
        bg, fg, goesFirst, degree = sys.argv[2:]
        TicTacToe(bg=bg, fg=fg, goesFirst=goesFirst, degree=degree).mainloop()

