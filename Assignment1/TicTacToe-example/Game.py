import Board
from numpy import zeros, transpose, where, random, mean

rng = random.default_rng()   # The random number generator


STRATEGY_RANDOM = 0
STRATEGY_SMART = 1

# return the next move, according to the specified strategy
def nextMove(board, strategy):  
    moves = board.getPossibleMoves()    
    if strategy == STRATEGY_RANDOM:  # Random move
        #return moves[rng.choice(len(moves))]
        return rng.choice(moves)
    else:       # Smart
        player = board.getPlayerTurn()
        for i in range(len(moves)):
            m = moves[i]
            b = board.copy()
            b.makeMove(m[0], m[1])
            s = b.evaluate()
            if ((s == Board.PLAYER1WINS and player == 1) 
                or (s == Board.PLAYER2WINS and player == 2)): 
                return m  # do the move, because the player will win
        # apparently, there was no move that results in a direct win
        # so do a random move
        return moves[rng.choice(len(moves))]

# Play one game, starting on the specified board, 
# with the two player strategies.
def playGame(board, strategyPlayer1, strategyPlayer2):
    score = board.evaluate()
    while (score == Board.NOTFINISHED):  # play as long as the game is not finished
        player = board.getPlayerTurn()
        if player == 1:
            move = nextMove(board, strategyPlayer1)
        else:  # player 2
            move = nextMove(board, strategyPlayer2)
        board.makeMove(move[0], move[1])
        score = board.evaluate()
    return (score, board)


# Test the board class
b = Board()
print("Start of the game, player's turn: %i" % b.getPlayerTurn())
b.makeMove(1, 1)
b.makeMove(0, 0)
b.makeMove(1, 0)
b.makeMove(2, 2)
print(b)
finishStr = ["NOT FINISHED", "PLAYER 1 WINS", "PLAYER 2 WINS", "DRAW"]
print(finishStr[b.evaluate()])
print("Possible moves: " + str(b.getPossibleMoves()))
b.makeMove(1, 2)
print(b)
print(finishStr[b.evaluate()])

# Play one game of two players playing randomly
(score, board) = playGame(Board(), STRATEGY_RANDOM, STRATEGY_RANDOM)
print(finishStr[score])
print(board)

# Do multiple runs
nrRuns = 100000
simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(Board(), STRATEGY_RANDOM, STRATEGY_RANDOM)
    simResults[i] = sim[0]

print('Strategy: Random vs. Random')      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))

simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(Board(), STRATEGY_SMART, STRATEGY_RANDOM)
    simResults[i] = sim[0]
      
print('Strategy: Smart vs. Random')      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))

simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(Board(), STRATEGY_RANDOM, STRATEGY_SMART)
    simResults[i] = sim[0]
      
print('Strategy: Random vs. Smart')      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))

simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(Board(), STRATEGY_SMART, STRATEGY_SMART)
    simResults[i] = sim[0]
      
print('Strategy: Smart vs. Smart')      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))


b = Board()
b.makeMove(1, 1)
print('Strategy: Smart vs. Smart.')      
print('First move: ')
print(b)
simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(b.copy(), STRATEGY_SMART, STRATEGY_SMART)
    simResults[i] = sim[0]
      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))


b = Board()
b.makeMove(2, 1)
print('Strategy: Smart vs. Smart.')      
print('First move: ')
print(b)
simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(b.copy(), STRATEGY_SMART, STRATEGY_SMART)
    simResults[i] = sim[0]
      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))


b = Board()
b.makeMove(2, 2)
print('Strategy: Smart vs. Smart.')      
print('First move: ')
print(b)
simResults = zeros(nrRuns)
for i in range(nrRuns):
    sim = playGame(b.copy(), STRATEGY_SMART, STRATEGY_SMART)
    simResults[i] = sim[0]
      
print('Player 1 wins: %f' % mean(simResults == 1))
print('Player 2 wins: %f' % mean(simResults == 2))
print('Draw         : %f' % mean(simResults == 3))



