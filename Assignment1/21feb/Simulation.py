
from Board import Board
from Piece import Piece
from Game import Game
from numpy import zeros, mean, where

class Simulator:
    
    def Sim(board, boardpiece, boardcolor, columsMoves, strategy):
        nrRuns = 100
        results = zeros(nrRuns)
        nrMoves = zeros(nrRuns)
        extraQueens = zeros(nrRuns)
        for i in range(nrRuns):
            # copy the initial board and play a game on the copy
            cboard, cboardpiece, cboardcolor, ccolumsMoves  = Board.copy(board, boardpiece, boardcolor, columsMoves)
            result, nrMove, extraQueen = Game.playGame(cboard, cboardpiece, cboardcolor, ccolumsMoves, strategy)
            results[i] = result
            nrMoves[i] = nrMove
            extraQueens[i] = extraQueen
            print("Simulator board",board)
        print(results)
        print("Final results")
        print("Player 1 wins:", mean(results == 1))
        print("Player 2 wins:", mean(results == 2))
        print("Draw:", mean(results == 3))
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("Number of moves per game:", nrMoves)
        print("Average # of moves per game:", mean(nrMoves))
        
        indexWhiteWins = where(results==1)
        if len(indexWhiteWins)>0:
            nrMovesWhiteWins = []
            for i in indexWhiteWins:
                nrMovesWhiteWins.append(nrMoves[i])
                print("nrMovesWhiteWins:", nrMovesWhiteWins)
                print("mean # Moves White Wins:", mean(nrMovesWhiteWins))
        else:
            print("No wins for white")
        
        print(extraQueens)
        TimesExtraQueen = [i for i in extraQueens if i != 0]
        print("times that queen is added:",len(TimesExtraQueen))

        return "Simulation done"


b = Board()
print(Simulator.Sim(b.board, b.boardpiece, b.boardcolor, b.columsMoves, Piece.STRATEGY_RANDOM))
