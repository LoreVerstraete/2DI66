from numpy import array, zeros, where, transpose, prod, diag, append, flip
import numpy as np
import copy

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

    def copy(board, boardpiece, boardcolor, columsMoves):
        cboard = copy.copy(board)
        cboardpiece = copy.copy(boardpiece)
        cboardcolor = copy.copy(boardcolor)
        ccolumsMoves = copy.copy(columsMoves)
        return cboard, cboardpiece, cboardcolor, ccolumsMoves   
            
    def getPlayerTurn(nrMoves):
        return (nrMoves % 2) + 1   
        
    def __str__(self):
        s = ""
        charscolor = ["_", "W", "B"]
        charspiece = ["_", "P", "R", "H", "B", "Q", "K"]   
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                s += charscolor[int(self.boardcolor[i,j])] + charspiece[int(self.boardpiece[i,j])] + " "
            s += "\n" 
        return s

b = Board()
# print(b)
# cboard, cboardpiece, cboardcolor, ccolumsMoves  = b.copy(b.boardpiece, b.boardcolor, b.columsMoves)
# print("copy", b.copy(b.boardpiece, b.boardcolor, b.columsMoves))
# print("cboard", cboard)
# print("cboardpiece", cboardpiece)
# print("cboardcolor", cboardcolor)
# print("ccolumsmoves", ccolumsMoves)
#x = b.firstRow()
# print(b.copy())
# cboard, cboardpiece, cboardcolor, ccolumsMoves = b.copy()
# print(cboard)
# print(b.boardpiece)
# print(len(where(b.boardpiece ==6)))