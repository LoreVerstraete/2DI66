from numpy import zeros, where, transpose, prod, diag, append


class Board:
    
    SIZE = 3
    NOTFINISHED = 0;   # Game is not finished (yet)
    PLAYER1WINS = 1;   # Game ends in a win for player 1
    PLAYER2WINS = 2;   # Game ends in a win for player 2
    DRAW = 3;          # Game ends in a draw
        
    def __init__(self):
        self.board = zeros((self.SIZE, self.SIZE))
        
    def copy(self):
        c = Board()
        c.board = self.board.copy()
        return c    
        
    def getPossibleMoves(self):
        moves = (self.board == 0)
        return transpose(where(moves))
        
    def getPlayerTurn(self):
        nrSquares = self.SIZE**2
        nrEmptySquares = len(self.getPossibleMoves())
        nrMoves = nrSquares - nrEmptySquares
        return (nrMoves % 2) + 1
    
    def makeMove(self, row, col):
        self.board[row, col] = self.getPlayerTurn()

    def evaluate(self):
        rowProds = prod(self.board, axis=1)
        colProds = prod(self.board, axis=0)
        diag1prod = prod(diag(self.board))
        diag2prod = prod(diag(self.board[::-1]))
        prods = append(rowProds, colProds)
        prods = append(prods, [diag1prod, diag2prod])
        if (sum(prods == 1) > 0):
            return self.PLAYER1WINS
        elif (sum(prods == 2**self.SIZE) > 0):
            return self.PLAYER2WINS
        else:
            if len(self.getPossibleMoves()) == 0:
                return self.DRAW
            else:
                return self.NOTFINISHED        
        
    def __str__(self):
        s = ""
        chars = ["_", "X", "O"] # player 1 = X, player 2 = O
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                s += chars[int(self.board[i,j])] + " "
            s += "\n" 
        return s

b = Board()
print(b)
print(b.getPlayerTurn())
b.makeMove(1, 2)
print(b.getPlayerTurn())
print(b)
c = b.copy()
c.makeMove(1, 1)
print(b)
print(c)