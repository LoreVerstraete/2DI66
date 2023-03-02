#version 28-2-23
# Board: 
from numpy import array, zeros, where, transpose, prod, diag, append, flip
import numpy as np
import copy

class Board:
    
    SIZE = 5           # Size of the board

    
    # 1 = white player
    # 2 = black player
    # 0 = empty
    def __init__(self):
        # one initial board with the colors and pieces together
        self.board = array([[26, 25, 24, 23, 22],[21, 21, 21, 21, 21],[0, 0, 0, 0, 0],[11, 11, 11, 11, 11],[12, 13, 14, 15, 16]])
        # one initial board with only pieces
        self.boardpiece = array([[6, 5, 4, 3, 2],[1, 1, 1, 1, 1],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[2, 3, 4, 5, 6]])
        # one initial board with only the colors
        self.boardcolor = array([[2,2,2,2,2],[2,2,2,2,2],[0,0,0,0,0],[1,1,1,1,1],[1,1,1,1,1]])
        # to keep track of the number of column moves
        self.columsMoves = array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])


    # to make a copy of all boards defined above, used in the Game class to check if a move is allowed
    def copy(board, boardpiece, boardcolor, columsMoves):
        cboard = copy.copy(board)
        cboardpiece = copy.copy(boardpiece)
        cboardcolor = copy.copy(boardcolor)
        ccolumsMoves = copy.copy(columsMoves)
        return cboard, cboardpiece, cboardcolor, ccolumsMoves   
           
    # function to determine which players turn it is
    def getPlayerTurn(nrMoves):
        return (nrMoves % 2) + 1   
      
    # function to visualize the board
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