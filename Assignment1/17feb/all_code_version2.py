from numpy import array, zeros, where, transpose, prod, diag, append, flip
# import numpy as np

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
        self.nrMoves = 0

    def copy(self):
        c = Board()
        c.board = self.board.copy()
        return c    
        
    # def getPossibleMoves(self):
    #     moves = X

    def makeMove(self):
        self.nrMoves = self.nrMoves + 1
            
    def getPlayerTurn(self):
        return (self.nrMoves % 2) + 1   

    # def firstRow(self):
    #     return self.board[0][2]
    def reverseBoard(self):
        c = self.copy()
        Revboard = c.board[::-1,::-1]
        Revboardpiece = c.boardpiece[::-1,::-1]
        Revboardcolor = c.boardcolor[::-1,::-1]
        RevcolumsMoves = c.columsMoves[::-1,::-1]
        return Revboard,Revboardpiece,Revboardcolor,RevcolumsMoves
    
    # def reverseBoard(self):
    #     COPY = b.copy()
    #     REVERSEBOARD = COPY.board[::-1, ::-1]
    #     REVERSEPIECE = COPY.boardpiece[::-1, ::-1]
    #     REVERSECOLOR = COPY.boardcolor[::-1, ::-1]
    # REVERSEMOVES
    #     # print(original)
    #     # print(x)
    #     return REVERSEBOARD, REVERSEPIECE, REVERSECOLOR
        
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
# print(b)
# # x = b.firstRow()

# # print(b)
# # print(b)
# x = b.reverseBoard()
# print('x', x)
# # print(b)
# print(b.getPlayerTurn())
# b.makeMove()
# print(b.getPlayerTurn())
# b.makeMove()
# print(b.getPlayerTurn())
# b.makeMove()
# print(b.getPlayerTurn())
# print(b)

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
       if  column+1 < b.SIZE and boardcolor[row][column+1] != color: #and Check == False:    #move to the right
            moves.append((color, name, row, column+1, columsMoves, row, column))
       if 0 <= row+a < b.SIZE and boardcolor[row+a][column] != color :# and Check == False :      #move down / up 
            moves.append((color, name, row+a, column, columsMoves, row, column))
       if column > 0 and boardcolor[row][column-1] != color:# and Check == False :          #move to the left
            moves.append((color, name, row, column-1, columsMoves+1, row, column))
       if 0 <= row+a < b.SIZE and column+1 < b.SIZE and boardcolor[row+a][column+1] != color:# and Check == False :  #move diagonal down-right
            moves.append((color, name, row+a, column+1, columsMoves+1, row,column))
       if 0 <= row+a < b.SIZE and column > 0 and boardcolor[row+a][column-1] != color:#and Check == False : #move diagonal down-left
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
      print("PlayerTurn", Player)
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
print(b.board)
# print(Piece.KingMoves(b.board, 1, "P",1,1,5))
# print(Piece.allMoves(b.board, 2))
#print(Piece.allMoves(b.board))
# print(x)
# print(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves))
#print(Piece.allMoves(x[0], x[1], x[2], x[3]))
# # print(Piece.allMoves(b.reverseBoard[0]))

#%%
from Board import Board
from Piece import Piece
import numpy as np 
import random


class Game:
   
 ### start trying to code checkmate
  # def randomIndex(allMoves):
  #     amountOfMoves = len(allMoves)
  #     index = random.shuffle(list(np.range(amountOfMoves)))
      
  #     return index
  #     # else: 
  #     #     return index 
    
  # def randomStrategy(allMoves, index):
  #   if index == []: 
  #       return [] 
  #   else: 
        
  #       return allMoves[index[0]]
  
  # def checkmate():
      
  #     return a
  
  # def evaluate(allMoves, player):
  #     if allMoves == []:
  #         return b.DRAW
  #     if allMoves != [] and Game.checkmate == False:
  #         return b.NOTFINISHED
  #     if allMoves != [] and Game.checkmate == True:
  #         return player
      
  def randomStrategy(allMoves):
    amountOfMoves = len(allMoves)
    if amountOfMoves == 0: 
        return [] 
    else: 
        return allMoves[np.random.randint(amountOfMoves)]
    
    
  def MovePiece(board,boardpiece, boardcolor, columsMoves, randomStrategy):
      # changing the current position to empty
      board[randomStrategy[5]][randomStrategy[6]] = 0
      boardpiece[randomStrategy[5]][randomStrategy[6]] = 0
      boardcolor[randomStrategy[5]][randomStrategy[6]] = 0
      columsMoves[randomStrategy[5]][randomStrategy[6]] = 0
      
      # place the piece in the new position
      board[randomStrategy[2]][randomStrategy[3]] = randomStrategy[0]*10+randomStrategy[1]
      boardpiece[randomStrategy[2]][randomStrategy[3]] = randomStrategy[1]
      boardcolor[randomStrategy[2]][randomStrategy[3]] = randomStrategy[0]
      columsMoves[randomStrategy[2]][randomStrategy[3]] = randomStrategy[4]
      #moves.append((color, name, row+1, column-2, columsMoves+2, row, column))
      return board,boardpiece, boardcolor, columsMoves

  def playGame(board, boardpiece, boardcolor, columsMoves):
      score = 0#board.evaluate()
    
      while (score < 5):# board.NOTFINISHED):
          player = b.getPlayerTurn()
          if player == 1:
              print("Player 1")
              # print('score', score)
              allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)
              move = Game.randomStrategy(allMoves)
              board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
              b.makeMove()
              # b.nrMoves +=1
              #b.reverseBoard()#b.board, b.boardpiece, b.boardcolor, b.columsMoves)
              print(board)
              print("nr moves", b.makeMove)
          if player == 2:
              allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)
              move = Game.randomStrategy(allMoves)
              board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
              b.makeMove()
              #b.reverseBoard()#b.board, b.boardpiece, b.boardcolor, b.columsMoves)
              print('Player 2')
              # print('score', score)
              print(board)
              print("nr moves", b.nrMoves)
          score += 1 
              #board, boardpiece, boardcolor, columsMoves = b.reverseBoard(board, boardpiece, boardcolor, columsMoves)
          # break    
      

         
              

b = Board()
#p = Piece()
# print(b.board)
# print(Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves)))
# print(Game.MovePiece(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves))))
# print(Game.MovePiece(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves))))

print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves))


