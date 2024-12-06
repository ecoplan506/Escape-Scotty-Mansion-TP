import random
from types import SimpleNamespace

class Minefield:
    def __init__(app, rows, cols, mines):
        app.numOfMines = mines
        app.rows = rows
        app.cols = cols
        app.board = [[False for _ in range(app.cols)] for _ in range(app.rows)]
        
    def __repr__(app):
        str = ''
        for row in app.board:
            str += repr(row) + '\n'
        return str
    
    def __eq__(app, other):
        return app.board == other.board

    def checkNeighbors(app, r, c, seen):
        if (r >= len(app.board) or c >= len(app.board[0]) or 
                r < 0 or c < 0):
            return
        elif (r, c) in seen:
            return
        app.board[r][c] = app.countNeighbors(r, c)
        seen.add((r, c))
        if app.board[r][c] == None:
            app.checkNeighbors(r, c+1, seen)
            app.checkNeighbors(r+1, c, seen)
            app.checkNeighbors(r-1, c, seen)
            app.checkNeighbors(r, c-1, seen)
            app.checkNeighbors(r-1, c-1, seen)
            app.checkNeighbors(r+1, c+1, seen)
            app.checkNeighbors(r-1, c+1, seen)
            app.checkNeighbors(r+1, c-1, seen)
        else: 
            return

    def clearNeighbors(app, row, col):
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                testRow = row+drow
                testCol = col+dcol
                if testRow not in range(0, len(app.board)) or testCol not in range(0, len(app.board[0])):
                    continue
                if testRow == row and testCol == col:
                    continue
                test = app.board[testRow][testCol]
                valuesToPass = {'mine', 'flag'}
                if test in valuesToPass:
                    continue
                elif isinstance(test, bool) and test:
                    app.gameOver = True
                    app.timing = False
                elif test == None:
                    app.checkNeighbors(testRow, testCol, set())
                else:
                    app.board[testRow][testCol] = app.countNeighbors(testRow, testCol)
        
    def countNeighbors(app, row, col):
        count = 0
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                testRow = row+drow
                testCol = col+dcol
                if testRow not in range(0, len(app.board)) or testCol not in range(0, len(app.board[0])):
                    continue
                if testRow == row and testCol == col:
                    continue
                test = app.board[testRow][testCol]
                if type(test) == int:
                    continue
                if test or test == 'mine':
                    count += 1
        if count != 0:
            return count

    def noNeighboringMines(app, row, col):
        for drow in [-1, 0, 1]:
            for dcol in [-1, 0, 1]:
                testRow = row+drow
                testCol = col+dcol
                if testRow not in range(0, len(app.board)) or testCol not in range(0, len(app.board[0])):
                    continue
                test = app.board[testRow][testCol]
                if type(test) == bool and test:
                    return False
        return True

    def mineWin(app):
        count = 0
        for row in app.board:
            for v in row:
                if type(v) == bool or v == 'mine':
                    count += 1
        return count == app.numOfMines

    def generateField(app, row, col):
        firstClick = app.surroundingFirstClick(row, col)
        mines = 0
        while mines < app.numOfMines:
            randR = random.randrange(0, app.rows)
            randC = random.randrange(0, app.cols)
            if (randR,randC) in firstClick:
                continue
            elif not app.board[randR][randC]:
                app.board[randR][randC] = True
                mines += 1

    def surroundingFirstClick(app, row, col):
        firstClick = set()
        for dRow in [-1, 0 ,1]:
            for dCol in [-1, 0, 1]:
                firstClick.add((row+dRow, col+dCol))
        return firstClick
    
    def flag(app, row, col):
        cell = app.board[row][col]
        if type(cell) == int: 
            if not app.noNeighboringMines(row, col):
                return
            app.clearNeighbors(row, col)
        elif cell == 'mine':
            app.board[row][col] = True
        elif cell == 'flag':
            app.board[row][col] = False
        elif cell == False:
            app.board[row][col] = 'flag'
        elif cell == True:
            app.board[row][col] = 'mine'