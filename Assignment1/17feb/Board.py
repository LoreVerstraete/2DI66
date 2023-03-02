from numpy import array, zeros, where, transpose, prod, diag, append, flip
import numpy as np

class Board:
    
    SIZE = 5
    NOTFINISHED = 0;   # Game is not finished (yet)
    PLAYER1WINS = 1;   # Game ends in a win for white
    PLAYER2WINS = 2;   # Game ends in a win for black
    DRAW = 3;          # Game ends in a draw
        
    def __init__(self):
        self.board = array([[26, 25, 24, 23, 22],[21, 21, 21, 21, 21],[0, 0, 0, 0, 0],[11, 11, 11, 11, 11],[12, 13, 14, 15, 16]])
        self.boardpiece = array([[6, 5, 4, 3, 2],[1, 1, 1, 1, 1],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[2, 3, 4, 5, 6]])
        self.boardcolor = array([[2,2,2,2,2],[2,2,2,2,2],[0,0,0,0,0],[1,1,1,1,1],[1,1,1,1,1]])
        self.columsMoves = array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
        # kingplace = np.asmatrix(np.where(self.board == 25))
        # print(self.board)
        # print(self.boardcolor)
        # print(int(kingplace[1]))

    def copy(self):
        c = Board()
        c.board = self.board.copy()
        # c.boardpiece = self.boardpiece.copy()
        # c.boardcolor = self.boardcolor.copy()
        # c.columsMoves = self.columsMoves.copy()
        # return c.board, c.boardpiece, c.boardcolor, c.columsMoves   
        return c
            
    def getPlayerTurn(nrMoves):
        return (nrMoves % 2) + 1   

    def reverseBoard(self):
        c = self.copy()
        Revboard = c.board[::-1,::-1]
        Revboardpiece = c.boardpiece[::-1,::-1]
        Revboardcolor = c.boardcolor[::-1,::-1]
        RevcolumsMoves = c.columsMoves[::-1,::-1]
        return Revboard,Revboardpiece,Revboardcolor,RevcolumsMoves
        
    def __str__(self):
        s = ""
        # chars = ["__", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "WP", "WR", "WH", "WB", "WQ", "WK", " ", " ", " ", " ","BP","BR","BH","BB","BQ","BK"]   
        # for i in range(self.SIZE):
        #     for j in range(self.SIZE):
        #         s += chars[int(self.board[i,j])] + " "
        #     s += "\n" 
        # return s
        charscolor = ["_", "W", "B"]
        charspiece = ["_", "P", "R", "H", "B", "Q", "K"]   
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                s += charscolor[int(self.boardcolor[i,j])] + charspiece[int(self.boardpiece[i,j])] + " "
            s += "\n" 
        return s

b = Board()
print(b)
# x = b.firstRow()
print(b.copy())
cboard, cboardpiece, cboardcolor, ccolumsMoves = b.copy()
print(cboard)
