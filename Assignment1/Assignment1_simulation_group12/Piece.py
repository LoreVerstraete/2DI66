# Version 28-2-23
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
        while((column2+1) < b.SIZE and columsMoves2 < b.SIZE and board[row][column2+1]==0):
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