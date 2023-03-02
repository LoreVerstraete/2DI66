# version 27-2-23
# Board: 
from numpy import array, zeros, where, transpose, prod, diag, append, flip
import numpy as np
import copy

class Board:
    
    SIZE = 5           # Size of the board
    NOTFINISHED = 0;   # Game is not finished (yet)
    PLAYER1WINS = 1;   # Game ends in a win for white
    PLAYER2WINS = 2;   # Game ends in a win for black
    DRAW = 3;          # Game ends in a draw
        
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

#%%
#Piece: 
from Board import Board
import itertools
 
class Piece: 
    STRATEGY_RANDOM = 0
    STRATEGY_PAWN2 = 1
    # all pieces are given a number
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6
   
    
    # returns possible moves for Pawn
    def PawnMoves(board, boardcolor, color, name, row, column, columsMoves, a, strategy):
        moves = []
        
        # moving up (player 1) or down (player 2) in the same column (only possible when no piece is in that square)
        # if a square is within the board, and is empty
        if 0 <= row + a < b.SIZE and board[row+a][column] == 0: 
            #if it gets to the top (player1) or bottom (player2) row, the Pawn should be replaced with a Queen                                          
            if row+a == 0 or row+a == 4:
                # the column moves will be reset to 0
                columsMoves = 0
                # the possible move will be appended to the list of moves (this line is the same for all pieces)
                moves.append((color, Piece.Queen, row+a, column , columsMoves, row, column))
            #if the piece will not be in the last row, it is just a possible move
            else:                                                                
                moves.append((color, name, row+a, column, columsMoves, row, column))
        
        # moving diagonal to the right (only possible when opponent piece is in square)
        # TODO: other figure need to be deleted #moving diagonal, down-right --> this comment can be removed?
        # if square is witin the board, less than 5 column switches, the square is not empty and containing a piece of opponent player:
        if 0 <= row+a < b.SIZE and column+1 < b.SIZE and columsMoves < b.SIZE and board[row+a][column+1] != 0 and boardcolor[row+a][column+1] != color:                        
            if row+a == 0 or row+a == 4:                                                       
                columsMoves = 0
                moves.append((color, Piece.Queen, row+a, column+1, columsMoves, row, column))
            else:     
                #if the piece will not be in the last row, it is just a possible move                                                          
                moves.append((color, name, row+a, column+1, columsMoves+1, row, column))
        
        # moving diagonal to the left (only possible when opponent piece is in square)
        # if square is witin the board, less than 5 column switches, the square is not empty and containing a piece of opponent player:
        if 0 <= row+a < b.SIZE and column > 0 and columsMoves < b.SIZE and board[row+a][column-1] != 0 and boardcolor[row+a][column-1] != color:                           
            # if the pawn will be in the last row it is promoted to a queen:
            if row+a == 0 or row+a == 4:                                                       
                columsMoves = 0
                moves.append((color, Piece.Queen, row+a, column-1, columsMoves, row, column)) 
            #if the piece will not be in the last row, it is just a possible move
            else:                                                                
                moves.append((color, name, row+a, column-1, columsMoves+1, row, column))
        
        #strategy when pawn can move 2 squares at once for the first move
        if strategy == Piece.STRATEGY_PAWN2: 
            if color == 1: # only applicable for white
                if row == 3: # only applicable for initial position
                    if board[row+a][column] == 0 and board[row+2*a][column]==0:  #moving 2 up, same column when both unoccupied
                        moves.append((color, name, row+2*a, column, columsMoves, row, column))

        return moves            


    # returns possible moves for Rook
    def RookMoves(board, boardcolor, color, name, row, column, columsMoves, a):
        moves = [] 
        # for all possible directions:
            # while square within the boardsize, switches between columns < 5, and the suqare is empty, there is a possible move
            # if a square is within the boardsize, switches between columns < 5, not empty and containing a piece of the opponent player it is a possible move
            
        # defined per while loop, to make sure all while loops will start with the original information, and the original position is used in the move
        column1 = column
        columsMoves1 = columsMoves
        # moving to the left
        while(column1 > 0 and columsMoves1 < b.SIZE and board[row][column1-1]==0): 
                moves.append((color, name, row, column1-1, columsMoves1+1, row, column))
                #update the column, and columsMoves
                column1 = column1-1
                columsMoves1 = columsMoves1 + 1
        if column1 > 0 and columsMoves1 < b.SIZE and board[row][column1-1]!=0 and boardcolor[row][column1-1] != color:
                moves.append((color, name, row, column1-1, columsMoves1+1, row, column))
        
        column2 = column
        columsMoves2 = columsMoves
        # moving to the right
        while((column2+1) < b.SIZE and columsMoves2 < b.SIZE and board[row][column2+1]==0): ### check board[row][column2+1 or column2]
                moves.append((color, name, row, column2+1 , columsMoves2+1, row, column))
                #update the column, row, and columsMoves
                column2 = column2 + 1    
                columsMoves2 = columsMoves2 + 1 
        if column2+1 < b.SIZE and columsMoves2 < b.SIZE and board[row][column2+1]!=0 and boardcolor[row][column2+1] != color:
                moves.append((color, name, row, column2+1 , columsMoves2+1, row, column))
        
        row3 = row
        # moving up (player 1) or down (player 2)
        while(0 <= row3+a < b.SIZE and columsMoves < b.SIZE and board[row3+a][column]==0): 
            moves.append((color, name, row3+a, column , columsMoves, row, column))
            #update row
            row3 = row3 + a
        if 0 <= row3+a < b.SIZE and columsMoves < b.SIZE and board[row3+a][column]!=0 and boardcolor[row3+a][column] != color:
                moves.append((color, name, row3+a, column , columsMoves, row, column))

        return moves 


    # returns possible moves for Knight
    def KnightMoves(board, boardcolor, color, name, row, column, columsMoves, a):
        moves=[] 
        # for all possible directions:
            #if the square is wihtin the boardsize, less than 5 column switches, and not containing a piece of the player itself
            
        # moving 2 rows up (player 1) or down (player 2), and 1 column to the right
        if  0 <= row + (a*2) < b.SIZE and column +1 < b.SIZE and columsMoves < b.SIZE and boardcolor[row + a*2][column +1] != color: 
            moves.append((color, name, row+a*2, column+1, columsMoves+1, row, column))
        # moving 2 rows up (player 1) or down (player 2), and 1 column to the left
        if  0 <= row + (a*2) < b.SIZE and column > 0 and columsMoves < b.SIZE and boardcolor[row + a*2][column -1] != color:
            moves.append((color, name, row+a*2, column-1, columsMoves+1, row, column))
        # moving 1 row up (player 1) or down (player 2), and 2 columns to the right
        if  0 <= row +a < b.SIZE and column +2 < b.SIZE and columsMoves < b.SIZE and boardcolor[row + a][column +2] != color:
            moves.append((color, name, row+a, column+2, columsMoves+2, row, column))
        # moving 1 row up (player 1) or down (player 2), and 2 columns to the left
        if  0 <= row +a < b.SIZE and column -2 >= 0 and columsMoves < b.SIZE and boardcolor[row + a][column -2] != color:
            moves.append((color, name, row+a, column-2, columsMoves+2, row, column))
        return moves
    
    
    # returns possible moves for Bishop
    def BishopMoves(board, boardcolor, color, name, row, column, columsMoves, a):
        moves = [] 
        # for all possible directions:
            # while square within the boardsize, switches between columns < 5 and the suqare is empty, there is a possible move
            # if a square is within the boardsize, switches between columns < 5, not empty and containing a piece of the opponent player it is a possible move
        
        # defined per while loop, to make sure all while loops will start with the original information, and the original position is used in the move
        row1 = row
        column1 = column
        columsMoves1 = columsMoves
        # moving diagonal to the right, up (player 1) or down (player 2)
        while(0 <= row1+a < b.SIZE and column1+1 < b.SIZE and columsMoves1 < b.SIZE and board[row1+a][column1+1]==0):
            moves.append((color, name, row1+a, column1+1, columsMoves1+1, row, column))
            #update the column, row, and columsMoves
            column1, row1 = column1 + 1, row1 + a 
            columsMoves1 = columsMoves1 + 1
        if 0 <= row1+a < b.SIZE and column1+1 < b.SIZE and columsMoves1 < b.SIZE and board[row1+a][column1+1]!=0 and boardcolor[row1+a][column1+1] != color:
            moves.append((color, name, row1+a, column1+1, columsMoves1+1, row, column)) 
         
        row2 = row
        column2 = column
        columsMoves2 = columsMoves
        # moving diagonal to the left, up (player 1) or down (player 2)
        while(0 <= row2+a < b.SIZE and column2 > 0 and columsMoves2 < b.SIZE and  board[row2+a][column2-1]==0):
            moves.append([color, name, row2+a, column2-1 , columsMoves2+1, row, column])
            # update column, row, and columsMoves
            column2, row2 = column2 - 1, row2 +a
            columsMoves2 = columsMoves2 + 1
        if 0 <= row2+a < b.SIZE and column2 > 0 and columsMoves2 < b.SIZE  and board[row2+a][column2-1]!=0 and boardcolor[row2+a][column2-1] != color:
            moves.append((color, name, row2+a, column2-1, columsMoves2+1, row, column)) 
        
        return moves 
    
   
    # returns possible moves Queen
    def QueenMoves(board, boardcolor, color, name, row, column, columsMoves, a):
        moves = []
        # for all possible directions:
            # while square within the boardsize, switches between columns < 5 and the suqare is empty, there is a possible move
            # if a square is within the boardsize, switches between columns < 5, not empty and containing a piece of the opponent player it is a possible move
        
        # defined per while loop, to make sure all while loops will start with the original information, and the original position is used in the move
        column1 = column
        columsMoves1 = columsMoves
        # Move to the right
        while(column1 +1 < b.SIZE and columsMoves1 < b.SIZE and board[row][column1+1]==0):   
            moves.append((color, name, row, column1+1, columsMoves1+1, row, column))
            # update column and columsMoves
            column1 = column1+1
            columsMoves1 = columsMoves1 + 1
        if column1+1 < b.SIZE and columsMoves1 < b.SIZE and board[row][column1+1]!=0 and boardcolor[row][column1+1] != color:
            moves.append((color, name, row, column1+1, columsMoves1+1, row, column)) 
            
        row2 = row
        # Move up (player 1) or down (player 2)
        while(0 <= row2+a < b.SIZE and columsMoves < b.SIZE and board[row2+a][column]==0):
            moves.append((color, name, row2+a, column , columsMoves, row, column))
            # update row
            row2 = row2 + a
        if 0 <= row2+a < b.SIZE and columsMoves < b.SIZE and board[row2+a][column]!=0 and boardcolor[row2+a][column] != color:
            moves.append((color, name, row2+a, column, columsMoves, row, column)) 
            
        column3 = column
        columsMoves3 = columsMoves
        # Move to the left 
        while(column3 > 0 and columsMoves3 < b.SIZE and board[row][column3-1]==0):
            moves.append((color, name, row, column3-1 , columsMoves3+1, row, column))
            # update column and columsMoves
            column3 = column3 - 1
            columsMoves3 = columsMoves3 + 1
        if column3 > 0 and columsMoves3 < b.SIZE and board[row][column3-1]!=0 and boardcolor[row][column3-1] != color:
            moves.append((color, name, row, column3-1, columsMoves3+1, row, column)) 
            
        column4 = column
        row4 = row
        columsMoves4 = columsMoves
        # Move diagonal to the right, up (player 1) or down (player 2)
        while(0 <= row4 +a < b.SIZE and column4 + 1 < b.SIZE and columsMoves4 < b.SIZE and  board[row4+a][column4+1]==0):
            moves.append((color, name, row4+a, column4+1, columsMoves4+1, row, column))
            # update column, row, and columsMoves
            column4, row4 = column4 + 1, row4 + a    
            columsMoves4 = columsMoves4 + 1 
        if 0 <= row4+a < b.SIZE and column4+1 < b.SIZE and columsMoves4 < b.SIZE and board[row4+a][column4+1]!=0 and boardcolor[row4+a][column4+1] != color:
            moves.append((color, name, row4+a, column4+1, columsMoves4+1, row, column)) 
            
        column5 = column
        row5 = row
        columsMoves5 = columsMoves
        # Move diagonal to the left, up (player 1) or down (player 2)
        while(0 <= row5 +a < b.SIZE  and column5 > 0 and columsMoves5 < b.SIZE and  board[row5+a][column5-1]==0):# moving diagonal left-down
            moves.append((color, name, row5+a, column5-1, columsMoves5+1, row, column))
            # update column, row, and columsMoves
            column5, row5 = column5 - 1, row5 +a
            columsMoves5 = columsMoves5 + 1
        if 0 <= row5+a < b.SIZE and column5 > 0 and columsMoves5 < b.SIZE  and board[row5+a][column5-1]!=0 and boardcolor[row5+a][column5-1] != color:
            moves.append((color, name, row5+a, column5-1, columsMoves5+1, row, column)) 
            
        return moves 
    


    def KingMoves(board, boardcolor, color, name, row, column, columsMoves, a):
        #Check = Checkmate(board, color, name, row, column, columsMoves)
        moves = []
        # for all possible directions:
            # if square within boardsize, column switches < 5, square not containing piece of player itself:
        
        # Move to the right
        if column+1 < b.SIZE and columsMoves < b.SIZE and boardcolor[row][column+1] != color: #and Check == False:    #move to the right
                moves.append((color, name, row, column+1, columsMoves+1, row, column))
        # Move up (player 1) or down (player 2)
        if 0 <= row+a < b.SIZE and boardcolor[row+a][column] != color :# and Check == False :      #move down / up 
                moves.append((color, name, row+a, column, columsMoves, row, column))
        # Move to the left
        if column > 0 and columsMoves < b.SIZE and boardcolor[row][column-1] != color:# and Check == False :          #move to the left
                moves.append((color, name, row, column-1, columsMoves+1, row, column))
        # Move diagonal to the right, up (player 1) or down (player 2)
        if 0 <= row+a < b.SIZE and column+1 < b.SIZE and columsMoves < b.SIZE and boardcolor[row+a][column+1] != color:# and Check == False :  #move diagonal down-right
                moves.append((color, name, row+a, column+1, columsMoves+1, row,column))
        # Move diagonal to the left, up (player 1) or down (player 2)   
        if 0 <= row+a < b.SIZE and column > 0  and columsMoves < 5 and boardcolor[row+a][column-1] != color:#and Check == False : #move diagonal down-left
                moves.append((color, name, row+a, column-1, columsMoves+1, row, column))
        return moves
    

    # returns list with all possible moves
    def allMoves(board, boardpiece, boardcolor, columsMoves, Player, strategy):
        allMoves = []
        
        # if player 1 turn a = -1 and the pieces will move up
        if Player == 1:
            a = -1   
        # if player 2 turn a = 1 and the pieces will move down
        if Player ==2:
            a = 1 
        
        # go through the board and for every square containing a piece of the current player find all moves
        for row in range(b.SIZE):
            for column in range(b.SIZE):
                if boardcolor[row][column] == Player:
                    if boardpiece[row][column] == Piece.King:   #6
                        allMoves.append(Piece.KingMoves(board, boardcolor, Player, Piece.King, row, column, columsMoves[row][column], a))
                    if boardpiece[row][column] == Piece.Queen:  #5
                        allMoves.append(Piece.QueenMoves(board, boardcolor, Player, Piece.Queen, row, column, columsMoves[row][column], a))
                    if boardpiece[row][column] == Piece.Bishop: #4
                        allMoves.append(Piece.BishopMoves(board, boardcolor, Player, Piece.Bishop, row, column, columsMoves[row][column], a))
                    if boardpiece[row][column] == Piece.Knight: #3
                        allMoves.append(Piece.KnightMoves(board, boardcolor, Player, Piece.Knight, row, column, columsMoves[row][column], a))
                    if boardpiece[row][column] == Piece.Rook:   #2
                        allMoves.append(Piece.RookMoves(board, boardcolor, Player, Piece.Rook, row, column, columsMoves[row][column], a))
                    if boardpiece[row][column] == Piece.Pawn:   #1
                        allMoves.append(Piece.PawnMoves(board, boardcolor, Player, Piece.Pawn, row, column, columsMoves[row][column], a, strategy))
        allMoves = [x for x in allMoves if x !=[]]
        allMoves = list(itertools.chain(*allMoves))
        return allMoves


b = Board()

#%%
# Game: 
from Board import Board
from Piece import Piece
import numpy as np 
import random


class Game:
    
    # determine opponent
    def opp(player):
        return (player % 2) + 1

    # determine location of the king of the player
    def kingplace(boardpiece,boardcolor,player):
        KingPlaces = np.asmatrix(np.where(boardpiece == 6))
        PlayerPlaces = np.asmatrix(np.where(boardcolor == player))
        for i in range(np.shape(KingPlaces)[1]):
            for j in range(np.shape(PlayerPlaces)[1]):
                if KingPlaces[(0,i)]== PlayerPlaces[(0,j)] and KingPlaces[(1,i)] == PlayerPlaces[(1,j)]:
                    KingPlayer =((KingPlaces[(0,i)]), (KingPlaces[(1,i)]))
        return KingPlayer

    def check(board, boardpiece, boardcolor, columsMoves, player, strategy):
        # determine location of king 
        KingPlayer = Game.kingplace(boardpiece,boardcolor,player)

        # determine all moves of the opponent
        opponent = Game.opp(player)
        allMovesOpponent = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, opponent, strategy)
        ListCheck = []

        # determine for all opponent moves if the king will be in check
        for i in range(len(allMovesOpponent)):
            if KingPlayer[0] == allMovesOpponent[i][2] and KingPlayer[1] == allMovesOpponent[i][3]:
                ListCheck.append("True") # if the king is in check append True
            else:
                ListCheck.append("False") # if the king is not in check append False
            
        # determine if at least one move of the oponent will capture the king
        if ListCheck.count("True") > 0:
            check = True
                
        # when there is no true value, the opponent cannot capture the king, if the current player makes a certain move
        if ListCheck.count("True") == 0:
            check = False
        
        return check


    ########## check if by making a certain move the current player is in check
    def checkMoves(board, boardpiece, boardcolor, columsMoves, player, allMovesCheck, strategy):
        check = True
        move = 0
        # while there are still moves left and by moving the current player is in check keep going
        while allMovesCheck != [] and check == True:
            # determine one possible move from the list
            PosMove = Game.pickMove(allMovesCheck)

            print("All possible moves:")
            print(allMovesCheck)
            print("possible move:", PosMove)

            # copy the board in order to test the move
            cboard, cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
            print("board before move")
            print(cboard)

            # make the move on the copied board
            cboard, cboardpiece, cboardcolor, ccolumsMoves = Game.MovePiece(cboard,cboardpiece, cboardcolor, ccolumsMoves, PosMove)
            print("board after move:")
            print(cboard)

            # look up if the game is in check after the move
            check = Game.check(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, strategy)
            print("check:",check)

            # if the move results in a check, the move is not possible and will be removed from the list of moves
            if check:
                allMovesCheck.remove(PosMove)
            # if the move is possible, the move will be used in the game
            else:
                move = PosMove
            
        # If no available moves, as a default the king will move to its own place (so no move) and check will stay True   
        if allMovesCheck == []:
            KingPlayer = Game.kingplace(boardpiece,boardcolor,player)
            move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
        
        return check, move, allMovesCheck
    
    # choose a move randomly from the list of moves
    def pickMove(allMoves):
          amountOfMoves = len(allMoves)
          if amountOfMoves == 0: 
              return [] 
          else: 
              PosMove = allMoves[np.random.randint(amountOfMoves)]
              return PosMove
    
   
    # Make the move
    def MovePiece(board,boardpiece, boardcolor, columsMoves, move):
        # remove the piece from the old position
        board[move[5]][move[6]] = 0
        boardpiece[move[5]][move[6]] = 0
        boardcolor[move[5]][move[6]] = 0
        columsMoves[move[5]][move[6]] = 0
        
        # place the piece in the new position
        board[move[2]][move[3]] = move[0]*10+move[1]
        boardpiece[move[2]][move[3]] = move[1]
        boardcolor[move[2]][move[3]] = move[0]
        columsMoves[move[2]][move[3]] = move[4]

        return board,boardpiece, boardcolor, columsMoves

    # evaluate the game
    def evaluate(check_beforemove, NoMovesPossible, player):
        # if no check before and after the move, game is not finished
        if NoMovesPossible == False:
            return b.NOTFINISHED
        # if player is not in check before move and does not have possible moves, it is a draw
        elif check_beforemove == False and NoMovesPossible == True:
            return b.DRAW
        # if check before move can not be removed by a move, it is checkmate and opponent wins
        elif check_beforemove == True and NoMovesPossible == True and player == 1:
            return b.PLAYER2WINS
        elif check_beforemove == True and NoMovesPossible == True and player == 2:
            return b.PLAYER1WINS
        
    # play the game
    def playGame(board, boardpiece, boardcolor, columsMoves,strategy):
        states = ["Not finished yet", "Player 1 wins", "Player 2 wins", "Draw"]
        score = b.NOTFINISHED
        nrMoves = 0
        extraQueen = 0
        nrQueensold = 2
        nrQueensOld = 1
        # play until the game is finished
        while score == b.NOTFINISHED:
            print("board")
            print(board)
            # determine which player's turn is is
            player = Board.getPlayerTurn(nrMoves)

            for i in range(2):
                if player == i+1:
                    print("Turn of player", player)
                    # determine if the player is in check before the move
                    check_beforemove = Game.check(board, boardpiece, boardcolor, columsMoves, player, strategy)
                    # print("Player", player, "in check before move?",check_beforemove)
 
                    # determine all valid moves the player can do
                    allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player, strategy)
                    print("All Moves player ",player,":",allMoves)
                    NoMovesPossible, move, allMoves  = Game.checkMoves(board, boardpiece, boardcolor, columsMoves, player, allMoves, strategy)
                    
                    # execute the valid move
                    board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
                    print("Player", player, "has no possible moves?",NoMovesPossible)
                    print("move:",move)
                    
                    # determine amount of queens in the game
                    nrQueensnew = np.count_nonzero(boardpiece == 5)
                    print("nrQueensNEW", nrQueensnew)
                    #check if extra queen is added
                    if nrQueensnew > nrQueensold:
                        extraQueen += 1
                    nrQueensold = nrQueensnew
                    print("extraQueen", extraQueen)
                    
                    # evaluate the state of the game
                    score = Game.evaluate(check_beforemove, NoMovesPossible, player)
                
            nrMoves += 1 
            print("state of the game:", states[score])
            print("nr moves:", nrMoves)
            print('########################################################################')
        print("Final result:",states[score])
        print("Total number of moves:", nrMoves)

        return score, nrMoves, extraQueen
    
b = Board()
# print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves,Piece.STRATEGY_PAWN2))
print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves,Piece.STRATEGY_RANDOM))

#%%
# Simulation: 
from Board import Board
from Piece import Piece
from Game import Game
from numpy import zeros, mean, where, sqrt, var, std
from statsmodels.stats.weightstats import DescrStatsW
import time

class Simulator:
    
    def Sim(board, boardpiece, boardcolor, columsMoves, strategy):
        nrRuns = 100
        results = zeros(nrRuns)
        nrMoves = zeros(nrRuns)
        extraQueens = zeros(nrRuns)
        start_time = time.time()
        for i in range(nrRuns):
            # copy the initial board and play a game on the copy
            cboard, cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
            result, nrMove, extraQueen = Game.playGame(cboard, cboardpiece, cboardcolor, ccolumsMoves, strategy)
            results[i] = result
            nrMoves[i] = nrMove
            if extraQueen > 0:
                extraQueens[i] = 1
            # extraQueens[i] = extraQueen
            # print("Simulator board",board)
            print("run number", i)
        print(results)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("Question 1 (both random) / 4 (Pawn white)")
        print("Player 1 wins:", mean(results == 1))
        lb1 = mean(results==1) - 1.96*sqrt(var(results==1)/nrRuns)
        ub1 = mean(results==1) + 1.96*sqrt(var(results==1)/nrRuns)
        print("Confidence interval manually", lb1, ",", ub1)
        ci1 = DescrStatsW(results==1).tconfint_mean(alpha=0.05) 
        print("Confidence interval player 1 using function")
        print(ci1)
        print("  ")
        print("Player 2 wins:", mean(results == 2))
        lb2 = mean(results==2) - 1.96*sqrt(var(results==2)/nrRuns)
        ub2 = mean(results==2) + 1.96*sqrt(var(results==2)/nrRuns)
        print("Confidence interval manually", lb2, ",", ub2)
        ci2 = DescrStatsW(results==2).tconfint_mean(alpha=0.05) 
        print("Confidence interval player 2 using function")
        print(ci2)
        print("  ")
        print("Draw:", mean(results == 3))
        lb3 = mean(results==3) - 1.96*sqrt(var(results==3)/nrRuns)
        ub3 = mean(results==3) + 1.96*sqrt(var(results==3)/nrRuns)
        print("Confidence interval manually", lb3, ",", ub3)
        ci3 = DescrStatsW(results==3).tconfint_mean(alpha=0.05) 
        print("Confidence interval draw using function")
        print(ci3)
        print("  ")
        
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("Question 2")
        print(extraQueens)
        print("Probability a queen is added:", mean(extraQueens==1))
        lb4 = mean(extraQueens==1) - 1.96*sqrt(var(extraQueens)/nrRuns)
        ub4 = mean(extraQueens==1) + 1.96*sqrt(var(extraQueens)/nrRuns)
        print("Confidence interval using formula", lb4, ",",ub4)
        ci4 = DescrStatsW(extraQueens).tconfint_mean(alpha=0.05) 
        print("Confidence interval using function", ci4)
        print("  ")
        
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("Question 3")
        print("Number of moves per game:", nrMoves)
        print("Average # of moves per game:", mean(nrMoves))
        sigma = sqrt(var(nrMoves))
        print("std", std(nrMoves))
        print("sigma number of moves", sigma)
        print("Number runs needed", ((1.96*sigma)/0.01)**2)
        lb5 = mean(nrMoves) - 1.96*sqrt(var(nrMoves)/nrRuns)
        ub5 = mean(nrMoves) + 1.96*sqrt(var(nrMoves)/nrRuns)
        print("Confidence interval manually", lb5, ",", ub5)
        ci5 = DescrStatsW(nrMoves).tconfint_mean(alpha=0.05)
        print("Confidence interval number of moves with function", ci5)
        print("  ")
        indexWhiteWins = where(results==1)
        if len(indexWhiteWins)>0:
            nrMovesWhiteWins = []
            for i in indexWhiteWins:
                nrMovesWhiteWins.append(nrMoves[i])
                # print("nrMovesWhiteWins:", nrMovesWhiteWins)
                print("Mean number of moves when white wins:", mean(nrMovesWhiteWins))
                meanwins = mean(nrMovesWhiteWins)
                halfWidthWhite = 1.96 * sqrt(var(nrMovesWhiteWins)/nrRuns)
                print('Halfwidth for number of moves when white wins', halfWidthWhite)
                print('number runs needed', ((1.96*std(nrMovesWhiteWins))/0.01)**2)
                print("Confidence interval number of moves white wins", meanwins - halfWidthWhite, meanwins + halfWidthWhite)

            # ci6 = DescrStatsW(nrMovesWhiteWins).tconfint_mean(alpha=0.05)
            # print("Confidence interval number of moves if white wins", ci6)
        else:
            print("No wins for white")
        end_time = time.time()
        print('total time', end_time - start_time)

        return "Simulation done"


b = Board()
print(Simulator.Sim(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Piece.STRATEGY_RANDOM))