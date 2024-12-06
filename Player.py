import Graphic
import math

# draw player info
# player board = none debug

class Player:
    def __init__(self):
        self.playerBoard = None
        self.lives = 3

    def newGame(self):
        self.x = self.y = None
        self.currR = self.currC = None
        self.deactivating = False
        self.injury = False

    def move(self, dir):
        if dir == 'right' and self.currC < self.playerBoard.cols-1:
            dX, dY = 1, 0
        elif dir == 'left' and self.currC > 0:
            dX, dY = -1, 0
        elif dir == 'down' and self.currR < self.playerBoard.rows-1:
            dX, dY = 0, 1
        elif dir == 'up' and self.currR > 0:
            dX, dY = 0, -1
        else: return

        cell = self.playerBoard.validMove(self.currR, self.currC, dX, dY, dir)
        print(cell)
        print(self.playerBoard.board)
        if cell == 3: 
            self.currR += dY
            self.currC += dX
            return
        elif cell:
            self.deactivating = self.currR+dY, self.currC+dX 
            if cell == 1:
                self.injury = 1
                self.lives -= 1
              

class PlayerBoard:
    def __init__(self, minefield, edges):
        self.rows = len(minefield)
        self.cols = len(minefield[0])
        PlayerBoard.construct(self, edges, minefield)
        
    def construct(self, edges, minefield):
        self.board = [[(0, set()) for _ in range(self.cols)] for _ in range(self.rows)]
        for row, col, dir in edges:
            self.board[row][col][1].add(dir)
            if dir == 'right': dX, dY, oppositeDir = 1, 0, 'left'
            if dir == 'left': dX, dY, oppositeDir = -1, 0, 'right'
            if dir == 'down': dX, dY, oppositeDir = 0, 1, 'up'
            if dir == 'up': dX, dY, oppositeDir = 0, -1, 'down'
            self.board[row+dY][col+dX][1].add(oppositeDir)
        PlayerBoard.update(self, minefield)
    
    def update(self, minefield):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = minefield[row][col]
                if type(cell) == str:
                    PlayerBoard.reassign(self, row, col, 2)
                elif type(cell) == bool:
                    PlayerBoard.reassign(self, row, col, int(cell))
                elif type(cell) == int or cell == None:
                    PlayerBoard.reassign(self, row, col, 3)

    def validMove(self, r, c, dC, dR, dir):
        if dir in self.board[r][c][1]:
            return False
        return self.board[r+dR][c+dC][0]

    def reassign(self, r, c, value):
        mazeEdges = self.board[r][c][1]
        self.board[r][c] = (value, mazeEdges)


def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5
