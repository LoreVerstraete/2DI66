# Version 28-2-23
# Game: 
from Board import Board
from Piece import Piece
import numpy as np 
import random


class Game:
    
    NOTFINISHED = 0;   # Game is not finished (yet)
    PLAYER1WINS = 1;   # Game ends in a win for white
    PLAYER2WINS = 2;   # Game ends in a win for black
    DRAW = 3;          # Game ends in a draw
    
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

            # print("All possible moves:")
            # print(allMovesCheck)
            # print("possible move:", PosMove)

            # copy the board in order to test the move
            cboard, cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
            # print("board before move")
            # print(cboard)

            # make the move on the copied board
            cboard, cboardpiece, cboardcolor, ccolumsMoves = Game.MovePiece(cboard,cboardpiece, cboardcolor, ccolumsMoves, PosMove)
            # print("board after move:")
            # print(cboard)

            # look up if the game is in check after the move
            check = Game.check(cboard, cboardpiece, cboardcolor, ccolumsMoves, player, strategy)
            # print("check:",check)

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
            return Game.NOTFINISHED
        # if player is not in check before move and does not have possible moves, it is a draw
        elif check_beforemove == False and NoMovesPossible == True:
            return Game.DRAW
        # if check before move can not be removed by a move, it is checkmate and opponent wins
        elif check_beforemove == True and NoMovesPossible == True and player == 1:
            return Game.PLAYER2WINS
        elif check_beforemove == True and NoMovesPossible == True and player == 2:
            return Game.PLAYER1WINS
        
    # play the game
    def playGame(board, boardpiece, boardcolor, columsMoves,strategy):
        states = ["Not finished yet", "Player 1 wins", "Player 2 wins", "Draw"]
        score = Game.NOTFINISHED
        nrMoves = 0
        extraQueen = 0
        nrQueensold = 2
        nrQueensOld = 1
        # play until the game is finished
        while score == Game.NOTFINISHED:
            # print("board")
            # print(board)
            # determine which player's turn is is
            player = Board.getPlayerTurn(nrMoves)

            for i in range(2):
                if player == i+1:
                    # print("Turn of player", player)
                    # determine if the player is in check before the move
                    check_beforemove = Game.check(board, boardpiece, boardcolor, columsMoves, player, strategy)
                    # print("Player", player, "in check before move?",check_beforemove)
 
                    # determine all valid moves the player can do
                    allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player, strategy)
                    # print("All Moves player ",player,":",allMoves)
                    NoMovesPossible, move, allMoves  = Game.checkMoves(board, boardpiece, boardcolor, columsMoves, player, allMoves, strategy)
                    
                    # execute the valid move
                    board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
                    # print("Player", player, "has no possible moves?",NoMovesPossible)
                    # print("move:",move)
                    
                    # determine amount of queens in the game
                    nrQueensnew = np.count_nonzero(boardpiece == 5)
                    # print("nrQueensNEW", nrQueensnew)
                    #check if extra queen is added
                    if nrQueensnew > nrQueensold:
                        extraQueen += 1
                    nrQueensold = nrQueensnew
                    # print("extraQueen", extraQueen)
                   
                    # evaluate the state of the game
                    score = Game.evaluate(check_beforemove, NoMovesPossible, player)
                
            nrMoves += 1 
        #     print("state of the game:", states[score])
        #     print("nr moves:", nrMoves)
        #     print('########################################################################')
        # print("Final result:",states[score])
        # print("Total number of moves:", nrMoves)

        return score, nrMoves, extraQueen
    
b = Board()
print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves,Piece.STRATEGY_PAWN2))
#print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves,Piece.STRATEGY_RANDOM))