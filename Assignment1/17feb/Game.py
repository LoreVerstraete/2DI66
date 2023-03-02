from Board import *
from Piece import Piece
import numpy as np 
import random


class Game:
    #color, name, row5+a, column5-1, columsMoves+1, row, column
    STRATEGY_RANDOM = 0
    STRATEGY_SMART = 1

    def check(board, boardpiece, boardcolor, columsMoves, player):
        check = False
        opponent = (player % 2) + 1
        KingPlayer = np.asmatrix(np.where(board == player*10 + 6))
        allMovesOpponent = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, opponent)
        for i in range(len(allMovesOpponent)):
            if int(KingPlayer[0]) == allMovesOpponent[i][2]:
                if int(KingPlayer[1]) == allMovesOpponent[i][3]:
                    check = True
        return check
    
    # def evaluate(allMoves, player):
    #     if #checkmate == true -> player wins
    #     elif len(allMoves) == 0:
    #         score = 3 #no moves possible -> draw
    #     else:
    #         score = 0 #just going further
    #     return score

        # if allMoves == []:
        #     return b.DRAW
        # if allMoves != [] and Game.checkmate == False:
        #     return b.NOTFINISHED
        # if allMoves != [] and Game.checkmate == True:
        #     return player
        
    # def nextMove(allMoves,strategy): #add if in check it should uncheck it
    #     # if check == False:
    #         amountOfMoves = len(allMoves)
    #         if amountOfMoves == 0: 
    #             return [] 
    #         else: 
    #             checkDueToMove = False
    #             #move = random.choice(len(allMoves))
    #             move = allMoves[np.random.randint(amountOfMoves)]
    #             return move
    #     # else: # if check == True
    #     #     try :

    # return the next move, according to the specified strategy
    def nextMove(allMoves, strategy, board, boardpiece, boardcolor, columsMoves, player):
        STRATEGY_RANDOM = 0
        STRATEGY_START2 = 1 
        checkmate = False 
        if strategy == STRATEGY_RANDOM:  # Random move
            if len(allMoves) == 0: #check if moves are available
                move = []
            else:
                move = allMoves[np.random.randint(len(allMoves))]                   #random move
                cboard, cboardpiece, cboardcolor, ccolumsMoves = Board.copy()       #make copy of board
                Game.MovePiece(cboard, cboardpiece, cboardcolor, ccolumsMoves, move)    #make the move
                if Game.check(board, boardpiece, boardcolor, columsMoves, player) == False: #check if move will not lead to check
                    pass
                else: #if move goes to check, try the other moves
                    checkmate = player #default, if no move is possible to get it out of check, it will be checkmate. checkmate 2 means player 1
                    x = np.arange(len(allMoves))
                    np.random.shuffle(x)            #randomise order of moves
                    for i in x:
                        move = allMoves[i]                   
                        cboard, cboardpiece, cboardcolor, ccolumsMoves = board.copy()       #make copy of board
                        Game.MovePiece(cboard, cboardpiece, cboardcolor, ccolumsMoves, move)    #make the move
                        if Game.check(board, boardpiece, boardcolor, columsMoves, player) == False: #check if move will not lead to check
                            checkmate = False
            return move, checkmate
        else:       # Pawns could possibly start with 2 steps to the front
            print("SMART STRATEGY")
            # player = board.getPlayerTurn()
            # for i in range(len(moves)):
            #     m = moves[i]
            #     b = board.copy()
            #     b.makeMove(m[0], m[1])
            #     s = b.evaluate()
            #     if ((s == Board.PLAYER1WINS and player == 1) 
            #         or (s == Board.PLAYER2WINS and player == 2)): 
            #         return m  # do the move, because the player will win
            # # apparently, there was no move that results in a direct win
            # # so do a random move
            # return moves[rng.choice(len(moves))]
        
        
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
        nrMoves = 0
        while (nrMoves < 1):# board.NOTFINISHED):
            player = Board.getPlayerTurn(nrMoves)
            check = Game.check(board, boardpiece, boardcolor, columsMoves, player)
            print("Check?",check)
            if player == 1:
                print("Player 1")
                allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)
                print(allMoves)
                move = Game.nextMove(allMoves, 0, board, boardpiece, boardcolor, columsMoves, player)
                board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
            if player == 2:
                print('Player 2')
                allMoves = Piece.allMoves(board, boardpiece, boardcolor, columsMoves, player)
                print(allMoves)
                move = Game.nextMove(allMoves, 0, board, boardpiece, boardcolor, columsMoves, player)
                board, boardpiece, boardcolor, columsMoves = Game.MovePiece(board, boardpiece, boardcolor, columsMoves, move)
            nrMoves += 1 
            print(board)
            # print("nr moves", nrMoves)
             


b = Board()
#p = Piece()
# print(b.board)
# print(Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves)))
# print(Game.MovePiece(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves))))
# print(Game.MovePiece(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Game.randomStrategy(Piece.allMoves(b.board, b.boardpiece, b.boardcolor, b.columsMoves))))

print(Game.playGame(b.board, b.boardpiece, b.boardcolor, b.columsMoves))

