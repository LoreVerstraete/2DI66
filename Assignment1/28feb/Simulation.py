
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