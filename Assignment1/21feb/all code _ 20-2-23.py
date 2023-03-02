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
        self.board = array([[26, 25, 24, 23, 22],[21, 0, 21, 21, 21],[0, 0, 0, 0, 0],[11, 11, 11, 11, 11],[12, 13, 14, 15, 16]])
        self.boardpiece = array([[6, 5, 4, 3, 2],[1, 0, 1, 1, 1],[0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[2, 3, 4, 5, 6]])
        self.boardcolor = array([[2,2,2,2,2],[2,2,2,2,2],[0,0,0,0,0],[1,1,1,1,1],[1,1,1,1,1]])
        self.columsMoves = array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
        # kingplace = np.asmatrix(np.where(self.board == 25))
        # print(self.board)
        # print(self.boardcolor)
        # print(int(kingplace[1]))

    # def copy(self):
    #     c = Board()
    #     c.board = self.board.copy()
    def copy(board, boardpiece, boardcolor, columsMoves):
        #c = Board()
        #cboard, cboardpiece, cboardcolor, ccolumsMoves = copy.copy(board, boardpiece, boardcolor, columsMoves)
        cboard = copy.copy(board)
        cboardpiece = copy.copy(boardpiece)
        cboardcolor = copy.copy(boardcolor)
        ccolumsMoves = copy.copy(columsMoves)
        return cboard, cboardpiece, cboardcolor, ccolumsMoves   
        # return c
            
    def getPlayerTurn(nrMoves):
        return (nrMoves % 2) + 1   

    # def reverseBoard(self):
    #     c = self.copy()
    #     Revboard = c.board[::-1,::-1]
    #     Revboardpiece = c.boardpiece[::-1,::-1]
    #     Revboardcolor = c.boardcolor[::-1,::-1]
    #     RevcolumsMoves = c.columsMoves[::-1,::-1]
    #     return Revboard,Revboardpiece,Revboardcolor,RevcolumsMoves
        
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

# b = Board()
# print(b)
# print("copy", b.copy(b.boardpiece, b.boardcolor, b.columsMoves))
# x = b.firstRow()
# print(b.copy())
# cboard, cboardpiece, cboardcolor, ccolumsMoves = b.copy()
# print(cboard)

#%%
from Board import Board
import itertools
 
class Piece: 
  SIZE = 5
  
  def PawnMoves(board, boardcolor, color, name, row, column, columsMoves, a):
      moves = []   #empty list of moves
      # return board[1]
      # print(b.board[2][1])
      # print(b.board)
      if 0 <= row + a < b.SIZE and board[row+a][column] == 0:                                            #moving down, same column
          if row+a == 0 or row+a == 4:                                                       #if it gets to the last row, the Pawn should be replaced with a Queen
              columsMoves = 0
              #moves.append((color, "Q" , row+a, column , columsMoves, row, column)) #changed Q to 5
              moves.append((color, 5 , row+a, column , columsMoves, row, column))
          else:                                                                #if the piece will not be in the last row, it is just a possible move
              moves.append((color, name, row+a, column, columsMoves, row, column))
              
      if 0 <= row+a < b.SIZE and column+1 < b.SIZE and columsMoves < b.SIZE and board[row+a][column+1] != 0 and boardcolor[row+a][column+1] != color:                       # TODO: other figure need to be deleted #moving diagonal, down-right
          if row+a == 0 or row+a == 4:                                                       #if it gets to the last row, the Pawn should be replaced with a Queen
              columsMoves = 0
              moves.append((color, 5 , row+a, column+1, columsMoves, row, column))
          else:                                                                #if the piece will not be in the last row, it is just a possible move
              moves.append((color, name, row+a, column+1, columsMoves+1, row, column))
                
      if 0 <= row+a < b.SIZE and column > 0 and columsMoves < b.SIZE and board[row+a][column-1] != 0 and boardcolor[row+a][column-1] != color:                           #moving diagonal down-left
          if row+a == 0 or row+a == 4:                                                       #if it gets to the last row, the Pawn should be replaced with a Queen
              columsMoves = 0
              moves.append((color, 5 , row+a, column-1, columsMoves, row, column)) 
          else:                                                                #if the piece will not be in the last row, it is just a possible move
              moves.append((color, name, row+a, column-1, columsMoves+1, row, column))

      return moves            

# b = Board()
# print(b)
# print(Piece.PawnMoves(b.board, b.boardcolor, 2, "P", 3,1,0))


  def RookMoves(board, boardcolor, color, name, row, column, columsMoves, a):
       moves = []                                                              # empty list of moves
       column1 = column# since 2 while loops are used, to make sure the second while loop will start with the original column number
       while(columsMoves < b.SIZE and column1 > 0 and board[row][column1-1]==0): #while the rook is not in the last and first column and if the square diagonal down-left is empty there is a possible move
            moves.append((color, name, row, column1-1, columsMoves+1, row, column))
            column1 = column1-1
       # print("a",columsMoves)
       if columsMoves < b.SIZE and column1 > 0 and board[row][column1-1]!=0 and boardcolor[row][column1-1] != color:
            moves.append((color, name, row, column1-1, columsMoves+1, row, column))
       column2 = column
       # print(b.board[2][4])
       
       while(columsMoves < b.SIZE and (column2+1) < b.SIZE and board[row][column2+1]==0): ### check board[row][column2+1 or column2]
            moves.append((color, name, row, column2+1 , columsMoves+1, row, column))
            column2 = column2 + 1
       if columsMoves < b.SIZE and column2+1 < b.SIZE and board[row][column2+1]!=0 and boardcolor[row][column2+1] != color:
            moves.append((color, name, row, column2+1 , columsMoves+1, row, column))
     
       while(columsMoves < b.SIZE and 0<= row+a < b.SIZE and board[row+a][column]==0): #while the rook is not in the last and first column and if the square diagonal down-left is empty there is a possible move
           moves.append((color, name, row+a, column , columsMoves, row, column))
           row = row + a
       if columsMoves < b.SIZE and 0 <= row+a < b.SIZE and board[row+a][column]!=0 and boardcolor[row+a][column] != color:
            moves.append((color, name, row+a, column , columsMoves, row, column))

       return moves 

# b = Board()
# print(b.board)
# print(Piece.RookMoves(b.board, 1, "P", 2,1,0))
  def KingMoves(board, boardcolor, color, name, row, column, columsMoves, a):
       #Check = Checkmate(board, color, name, row, column, columsMoves)
       moves = []
       if  column+1 < b.SIZE and columsMoves < b.SIZE and boardcolor[row][column+1] != color: #and Check == False:    #move to the right
            moves.append((color, name, row, column+1, columsMoves+1, row, column))
       if 0 <= row+a < b.SIZE and boardcolor[row+a][column] != color :# and Check == False :      #move down / up 
            moves.append((color, name, row+a, column, columsMoves, row, column))
       if column > 0 and  columsMoves < b.SIZE and boardcolor[row][column-1] != color:# and Check == False :          #move to the left
            moves.append((color, name, row, column-1, columsMoves+1, row, column))
       if 0 <= row+a < b.SIZE and column+1 < b.SIZE and columsMoves < b.SIZE and boardcolor[row+a][column+1] != color:# and Check == False :  #move diagonal down-right
            moves.append((color, name, row+a, column+1, columsMoves+1, row,column))
       if 0 <= row+a < b.SIZE and column > 0  and columsMoves < 5 and boardcolor[row+a][column-1] != color:#and Check == False : #move diagonal down-left
            moves.append((color, name, row+a, column-1, columsMoves+1, row, column))
       return moves
  

  def BishopMoves(board, boardcolor, color, name, row, column, columsMoves, a):
       moves = []
       row1 = row
       column1 = column
       while(column1+1 < b.SIZE and 0 <= row1+a < b.SIZE and columsMoves < b.SIZE and board[row1+a][column1+1]==0):
           moves.append((color, name, row1+a, column1+1, columsMoves+1, row, column))
           column1, row1 = column1 + 1, row1 + a 
       if columsMoves < b.SIZE and column1+1 < b.SIZE and 0 <= row1+a < b.SIZE and board[row+a][column1+1]!=0 and boardcolor[row+a][column1+1] != color:
           moves.append((color, name, row1+a, column1+1, columsMoves+1, row, column)) 
           
       while(columsMoves < b.SIZE and 0 <= row+a < b.SIZE and column > 0 and board[row+a][column-1]==0):
           moves.append([color, name, row+a, column-1 , columsMoves+1, row, column])
           column, row = column - 1, row +a
       if columsMoves < b.SIZE  and 0 <= row+a < b.SIZE and column > 0 and board[row+a][column-1]!=0 and boardcolor[row+a][column-1] != color:
           moves.append((color, name, row+a, column-1, columsMoves+1, row, column)) 
    
       return moves 

# b = Board()
# print(b.board)
# print(Piece.BishopMoves(b.board, 1, "P",1,4,0))

  def QueenMoves(board, boardcolor, color, name, row, column, columsMoves, a):
       moves = []
       column1 = column
       while(column1 +1 < b.SIZE and board[row][column1+1]==0):   #moving to the right
           moves.append((color, name, row, column1+1, columsMoves+1, row, column))
           column1 = column1+1
       if columsMoves < b.SIZE and column1+1 < b.SIZE and board[row][column1+1]!=0 and boardcolor[row][column1+1] != color:
           moves.append((color, name, row, column1+1, columsMoves+1, row, column)) 
           
       row2 = row
       while(columsMoves < b.SIZE and 0 <= row2+a < b.SIZE and board[row2+a][column]==0): # moving down
           moves.append((color, name, row2+a, column , columsMoves, row, column))
           row2 = row2 + a
       if columsMoves < b.SIZE  and 0 <= row2+a < b.SIZE and board[row2+a][column]!=0 and boardcolor[row2+a][column] != color:
               moves.append((color, name, row2+a, column, columsMoves, row, column)) 
           
       column3 = column
       while(columsMoves < b.SIZE and column3 > 0 and board[row][column3-1]==0): #moving to the left
           moves.append((color, name, row, column3-1 , columsMoves+1, row, column))
           column3 = column3 - 1
       if columsMoves < b.SIZE and column3 > 0 and board[row][column3-1]!=0 and boardcolor[row][column3-1] != color:
           moves.append((color, name, row, column3-1, columsMoves+1, row, column)) 
           
       column4 = column
       row4 = row
       while(columsMoves < b.SIZE and 0 <= row4 +a < b.SIZE and column4 + 1 < b.SIZE and board[row4+a][column4+1]==0): #moving diagonal right-down
           moves.append((color, name, row4+a, column4+1, columsMoves+1, row, column))
           column4, row4 = column4 + 1, row4 + a 
       if columsMoves < b.SIZE  and 0 <= row4+a < b.SIZE and column4+1 < b.SIZE and board[row4+a][column4+1]!=0 and boardcolor[row4+a][column4+1] != color:
           moves.append((color, name, row4+a, column4+1, columsMoves+1, row, column)) 
           
       column5 = column
       row5 = row
       while(columsMoves < b.SIZE and 0 <= row5 +a < b.SIZE  and column5 > 0 and board[row5+a][column5-1]==0):# moving diagonal left-down
           moves.append((color, name, row5+a, column5-1, columsMoves+1, row, column))
           column5, row5 = column5 - 1, row5 +a
       if columsMoves < b.SIZE  and 0 <= row5+a < b.SIZE and column5 > 0 and board[row5+a][column5-1]!=0 and boardcolor[row5+a][column5-1] != color:
           moves.append((color, name, row5+a, column5-1, columsMoves+1, row, column)) 
        
       return moves 

# b = Board()
# print(b.board)
# print(Piece.QueenMoves(b.board, 1, "P",2,0,0))

  def KnightMoves(board, boardcolor, color, name, row, column, columsMoves, a):
       moves=[]
       if  0 <= row + (a*2) < b.SIZE and column +1 < b.SIZE and boardcolor[row + a*2][column +1] != color: 
           moves.append((color, name, row+a*2, column+1, columsMoves+1, row, column))
       if  0 <= row + (a*2) < b.SIZE and column > 0 and boardcolor[row + a*2][column -1] != color:
           moves.append((color, name, row+a*2, column-1, columsMoves+1, row, column))
       if  0 <= row +a < b.SIZE and column +2 < b.SIZE and boardcolor[row + a][column +2] != color:
           moves.append((color, name, row+a, column+2, columsMoves+2, row, column))
       if  0 <= row +a < b.SIZE and column -2 >= 0 and boardcolor[row + a][column -2] != color:
           moves.append((color, name, row+a, column-2, columsMoves+2, row, column))
       return moves

   
  def allMoves(board, boardpiece, boardcolor, columsMoves, Player):
      allMoves = []
      #Player = b.getPlayerTurn()
      #print("PlayerTurn", Player)
      if Player == 1:#b.getPlayerTurn == 1:
         a = -1   
      if Player ==2:#b.getPlayerTurn == 2:
         a = 1 
      # print("Player", Player)
      for row in range(b.SIZE):
          for column in range(b.SIZE):
              if boardcolor[row][column] == Player:
                  if boardpiece[row][column] == 6:
                      #allMoves.append("King")
                      allMoves.append((Piece.KingMoves(board, boardcolor, Player, 6, row, column, columsMoves[row][column], a)))
                  if boardpiece[row][column] == 5:
                      #allMoves.append("Queen")
                      allMoves.append(Piece.QueenMoves(board, boardcolor, Player, 5, row, column, columsMoves[row][column], a))
                  if boardpiece[row][column] == 4:
                      allMoves.append(Piece.BishopMoves(board, boardcolor, Player, 4, row, column, columsMoves[row][column], a))
                  if boardpiece[row][column] == 3:
                      allMoves.append(Piece.KnightMoves(board, boardcolor, Player, 3, row, column, columsMoves[row][column], a))
                  if boardpiece[row][column] == 2:
                      allMoves.append(Piece.RookMoves(board, boardcolor, Player, 2, row, column, columsMoves[row][column], a))
                  if boardpiece[row][column] == 1:
                      allMoves.append(Piece.PawnMoves(board, boardcolor, Player, 1, row, column, columsMoves[row][column], a))
      allMoves = [x for x in allMoves if x !=[]]
      allMoves = list(itertools.chain(*allMoves))
      return allMoves
                     
                      
      

b = Board()
# x = b.reverseBoard()
#print(b.board)

# print(Piece.KingMoves(b.board, 1, "P",1,1,5))
# print(Piece.allMoves(b.board, 2))
#print(Piece.allMoves(b.board))
# print(x)
# print(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves, 1))
#print(Piece.allMoves(x[0], x[1], x[2], x[3]))
# # print(Piece.allMoves(b.reverseBoard[0]))

#%%
from Board import Board
from Piece import Piece
import numpy as np 
import random


class Game:

    STRATEGY_RANDOM = 0
    STRATEGY_SMART = 1
    
    ######### to check for checkmate to make the king make a certain move
    def checkmate(board, boardpiece, boardcolor, columsMoves, player, move):
        list_checkmate = []
        opponent = (player % 2) + 1
        # define all possible moves from opponent player before current player makes a move
        allMovesOpponent = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, opponent)
    
        # determine location of King
        for row in range(b.SIZE):
            for column in range(b.SIZE):
                if boardcolor[row][column] == player:
                    if boardpiece[row][column] == 6:
                        KingPlayer = row, column
        # KingPlayer = np.asmatrix(np.where(board == player*10 + 6))
        # print("Kingplayer checkmate, line 20", KingPlayer)#[1], type(KingPlayer))
        
        # check for all possible moves of the opponent player if the king will be in checkmate
        # and add to list 'true' if the opponent player can capture the king of the current player
        for m in range(len(allMovesOpponent)):
            if KingPlayer[0] == allMovesOpponent[m][2]:
                if KingPlayer[1] == allMovesOpponent[m][3]:
                    list_checkmate.append("True")
                    
        # check if at least one possible move can lead to capturing the king        
        if list_checkmate.count("True") > 0:
            return True
        
        # check if there is no possibility for the opponent player to capture the king
        if list_checkmate.count("True") == 0:
            return False
        
    ########## check if by making a certain move the current player is in check
    def check(board, boardpiece, boardcolor, columsMoves, player):
        check = True
        opponent = (player % 2) + 1
        move = 0
        # define a list of all moves of a copy board
        allMovesCheck = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)
        number = 0
        # while there are still moves left and by moving the current player is in check keep going
        while allMovesCheck != [] and check == True:

            # determine one possible move from the list
            PosMove = Game.randomStrategy(allMovesCheck)

            print("All possible moves:")
            print(allMovesCheck)
            print("Board",board)
            print("possible move, line 42", PosMove)
            # copy the board
            cboard,cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
            print("cboard before move")
            print(cboard)
            # make the move on the copied board
            cboard, cboardpiece, cboardcolor, ccolumsMoves = Game.checkMove(cboard, cboardpiece, cboardcolor, ccolumsMoves, PosMove)
            print("cboard after move:")
            print(cboard)
            # determine location of king
            for row in range(b.SIZE):
                for column in range(b.SIZE):
                    if cboardcolor[row][column] == player:
                        if cboardpiece[row][column] == 6:
                            KingPlayer = row, column
            # KingPlayer = np.asmatrix(np.where(cboard == player*10 + 6))
            # print("Kingplayer check, line 49", KingPlayer)#[1], type(KingPlayer))
            
            # determine all moves of the opponent
            allMovesOpponent = Piece.allMoves(cboard, cboardpiece, cboardcolor, ccolumsMoves, opponent)
            ListTrue = []

            # determine for all opponent moves if the king will be in check
            for i in range(len(allMovesOpponent)):
                for row in range(b.SIZE):
                    for column in range(b.SIZE):
                        if cboardcolor[row][column] == player:
                            if cboardpiece[row][column] == 6:
                                KingPlayer = row, column
                if KingPlayer[0] == allMovesOpponent[i][2]:
                    if KingPlayer[1] == allMovesOpponent[i][3]:
                        number+=1
                        ListTrue.append("True") # if the king is in check append True
                    else:
                        ListTrue.append("False") # if the king is not in check append False
            
            # determine if at least one move of the oponent will capture the king
            if ListTrue.count("True") > 0:
                check = True
                move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
                # if the move will make the opponent possible to capture the king remove the move
                allMovesCheck.remove(PosMove)
                print("not a possible move, line 65")
                print("all moves check remove PosMove")
                print(allMovesCheck)
                
                #when no moves are left, the opponent wins
                if allMovesCheck == []:
                    return check, move
                
            # when there is no true value, the opponent cannot capture the king, if the current player makes a certain move
            if ListTrue.count("True") == 0:
                move = PosMove
                print("there is a possible move", move)
                # check if the current player is already in check and should thus change the move
                g = Game.checkmate(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, move)

                if g  == False:
                    # the possible move will make sure the current player will not be in check and is not already in check
                    check = False
                    return  check, move
                if g == True: #Game.checkmate(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, move) == True:
                    # if the current player is already in check keep looking for another move
                    move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
                    check = True

                    return check, move
        if allMovesCheck == [] and check == True:
            for row in range(b.SIZE):
                for column in range(b.SIZE):
                    if boardcolor[row][column] == player:
                        if boardpiece[row][column] == 6:
                            KingPlayer = row, column
            move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
            return check, move
    # ########## check if by making a certain move the current player is in check
    # def check(cboard, cboardpiece, cboardcolor, ccolumsMoves, player):
    #     check = True
    #     opponent = (player % 2) + 1
    #     move = 0
    #     # define a list of all moves of a copy board
    #     allMovesCheck = Piece.allMoves(cboard, cboardpiece, cboardcolor, ccolumsMoves, player)
    #     number = 0
    #     # while there are still moves left and by moving the current player is in check keep going
    #     while allMovesCheck != [] and check == True:

    #         # determine one possible move from the list
    #         PosMove = Game.randomStrategy(allMovesCheck)
    #         print("possible move, line 42", PosMove)
    #         print("All possible moves:")
    #         print(allMovesCheck)
    #         print(cboard)
    #         # copy the board
    #         cboard,cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(b.board, b.boardpiece, b.boardcolor, b.columsMoves)

    #         # make the move on the copied board
    #         cboard, cboardpiece, cboardcolor, ccolumsMoves = Game.checkMove(cboard, cboardpiece, cboardcolor, ccolumsMoves, PosMove)

    #         # determine location of king
    #         for row in range(b.SIZE):
    #             for column in range(b.SIZE):
    #                 if cboardcolor[row][column] == player:
    #                     if cboardpiece[row][column] == 6:
    #                         KingPlayer = row, column
    #         # KingPlayer = np.asmatrix(np.where(cboard == player*10 + 6))
    #         # print("Kingplayer check, line 49", KingPlayer)#[1], type(KingPlayer))
            
    #         # determine all moves of the opponent
    #         allMovesOpponent = Piece.allMoves(cboard, cboardpiece, cboardcolor, ccolumsMoves, opponent)
    #         ListTrue = []

    #         # determine for all opponent moves if the king will be in check
    #         for i in range(len(allMovesOpponent)):
    #             if KingPlayer[0] == allMovesOpponent[i][2]:
    #                 if KingPlayer[1] == allMovesOpponent[i][3]:
    #                     number+=1
    #                     ListTrue.append("True") # if the king is in check append True
    #                 else:
    #                     ListTrue.append("False") # if the king is not in check append False
            
    #         # determine if at least one move of the oponent will capture the king
    #         if ListTrue.count("True") > 0:
    #             check = True
    #             move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
    #             # if the move will make the opponent possible to capture the king remove the move
    #             allMovesCheck.remove(PosMove)
    #             print("not a possible move, line 65")
    #             print(allMovesCheck)
                
    #             #when no moves are left, the opponent wins
    #             if allMovesCheck == []:
    #                 return check, move
                
    #         # when there is no true value, the opponent cannot capture the king, if the current player makes a certain move
    #         if ListTrue.count("True") == 0:
    #             move = PosMove
                
    #             # check if the current player is already in check and should thus change the move
    #             g = Game.checkmate(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, move)

    #             if g  == False:
    #                 # the possible move will make sure the current player will not be in check and is not already in check
    #                 check = False
    #                 return  check, move
    #             if g == True: #Game.checkmate(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, move) == True:
    #                 # if the current player is already in check keep looking for another move
    #                 move = (player, 6, KingPlayer[0], KingPlayer[1], 0, KingPlayer[0], KingPlayer[1])
    #                 check = True

    #                 return check, move

    # choose a move randomly from the list of moves
    def randomStrategy(allMoves):
          amountOfMoves = len(allMoves)
          if amountOfMoves == 0: 
              return [] 
          else: 
              PosMove = allMoves[np.random.randint(amountOfMoves)]
              return PosMove
    
    # copied board to check multiple moves
    def checkMove(board, boardpiece, boardcolor, columsMoves, randomStrategy): #cboard, cboardpiece, cboardcolor, ccolumsMoves, randomStrategy):
        cboard,cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
        
        # changing the current position to empty
        cboard[randomStrategy[5]][randomStrategy[6]] = 0
        cboardpiece[randomStrategy[5]][randomStrategy[6]] = 0
        cboardcolor[randomStrategy[5]][randomStrategy[6]] = 0
        ccolumsMoves[randomStrategy[5]][randomStrategy[6]] = 0
            
        # place the piece in the new position
        cboard[randomStrategy[2]][randomStrategy[3]] = randomStrategy[0]*10+randomStrategy[1]
        cboardpiece[randomStrategy[2]][randomStrategy[3]] = randomStrategy[1]
        cboardcolor[randomStrategy[2]][randomStrategy[3]] = randomStrategy[0]
        ccolumsMoves[randomStrategy[2]][randomStrategy[3]] = randomStrategy[4]

        return cboard, cboardpiece, cboardcolor, ccolumsMoves
    
    # real board to make the move
    def MovePiece(board,boardpiece, boardcolor, columsMoves, move):
        
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
    def evaluate(allMoves, player, board, boardpiece, boardcolor, columsMoves, move, check):
        # if no moves are left there is a draw
        if allMoves == []: # maybe add check == false and checkmate == false?
            return b.DRAW
        # if still moves left, and check is false and checkmate is false the game continues
        if allMoves != [] and check == False: # and Game.checkmate(board, boardpiece, boardcolor, columsMoves, player, move) == False:
            return b.NOTFINISHED
        # if it is player 1 turn but check is true or checkmate is true player 2 wins
        if player == 1:
            if check == True: #allMoves != [] and check == True:# or Game.checkmate(board, boardpiece, boardcolor, columsMoves, player, move) == True:
                return b.PLAYER2WINS
        # if it is player 2 turn but check is true or checkmate is true player 1 wins
        if player == 2:
            if check == True: #allMoves != [] and check == True:# or Game.checkmate(board, boardpiece, boardcolor, columsMoves, player, move) == True:
                return b.PLAYER1WINS

        
    # play the game
    def playGame(board, boardpiece, boardcolor, columsMoves):
        score = b.NOTFINISHED
        nrMoves = 0

        print(board)
        while score == 0: #nrMoves < 30: #score == b.NOTFINISHED:#(nrMoves < 30):# board.NOTFINISHED):
            print("board")
            print(board)
            player = Board.getPlayerTurn(nrMoves)

            if player == 1:
                print("Player 1")
                allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)

                move1 = Game.check(board, boardpiece, boardcolor, columsMoves, player)

                check_0 = move1[0]
                move = move1[1]

                score = Game.evaluate(allMoves, player, board, boardpiece, boardcolor, columsMoves, move, check_0)
                board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)

                print("score player 1, line 171", score)


 
            if player == 2:
                print('Player 2, line 176')
                allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)

                move2 = Game.check(board, boardpiece, boardcolor, columsMoves, player)

                check_0 = move2[0]
                move = move2[1]

                score = Game.evaluate(allMoves, player, board, boardpiece, boardcolor, columsMoves, move, check_0)
                board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
                
                print("score player 2, line 188", score)

            
            
            nrMoves += 1 
            # print(board)
            print("nr moves, line 193", nrMoves)
            print('########################################################################')


        if score == b.NOTFINISHED:
            return b.NOTFINISHED
        if score == b.PLAYER1WINS:
            return b.PLAYER1WINS
        if score == b.PLAYER2WINS:
            return b.PLAYER2WINS
        if score == b.DRAW:
            return b.DRAW
             


b = Board()

print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves))#, b.cboard, b.cboardpiece, b.cboardcolor, b.ccolumsMoves))


#%%
from Board import Board
from Piece import Piece
from Game import Game
from numpy import zeros, mean

class Simulator:
    
    def Sim(board, boardpiece, boardcolor, columsMoves):
        nrRuns = 1000
        results = zeros(nrRuns)
        #b = Board()

        

        for i in range(nrRuns):
            result = Game.playGame(board, boardpiece, boardcolor, columsMoves)
            results[i] = result
            print("Simulator board",board)
        print(results)
        print("resutls 1", mean(results == 1))
        print("results 2", mean(results == 2))
        print("results 3", mean(results == 3))


b = Board()
print(Simulator.Sim(b.board, b.boardpiece, b.boardcolor, b.columsMoves))
