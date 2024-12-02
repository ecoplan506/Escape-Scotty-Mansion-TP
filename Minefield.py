import random
from types import SimpleNamespace

# Bugs to Fix:
   # control instructions
   # mouse hover -> word movement

   
'''
   Controls:
   - Left-click an empty square to reveal it.
   - Right-click (or Ctrl+click) an empty square to flag it.
   - Midde-click (or left+right click) a number to reveal
     its adjacent squares.
   - Press space bar while hovering over a square to flag
     it or reveal its adjacent squares. 
   - Press r to restart.
     
'''


class Minefield:
    def __init__(app, rows, cols):
        app.rows = rows
        app.cols = cols
        app.cx = app.cy = 0
        app.difficulty = 'easy'
        app.instructions = True
        app.restart(app)
        
    def __repr__(app):
        str = ''
        for row in app.board:
            str += row + '\n'
        return str
    
    def __eq__(app, other):
        return app.board == other.board

    ##########################################################################
        
    def onMouseMove(app, mouseX, mouseY):
        app.cx = mouseX
        app.cy = mouseY

    def onMousePress(app, mouseX, mouseY):
        #restart after loss
        if app.gameOver:
            app.restart(app)
            return
        
        #restart after winning
        elif app.winner: return
        
        #play minesweeper
        else:
            if app.newBoard: 
                app.newBoard = False
                firstCell = app.getCell(app, app.cx, app.cy)
                firstClick = surroundingFirstClick(firstCell)
                app.board = generateField(app.rows, app.cols, app.numOfMines, firstClick)

            row, col = app.getCell(app, mouseX, mouseY)
            cell = app.board[row][col]
            
            if app.space:
                return
            elif cell == 'mine' or cell == 'flag' or type(cell) == int:
                return
            else:
                app.checkMine(app, row, col)

        if app.checkWin(app):
            app.winner = True
            
    def onKeyPress(app, key):
        if app.winner: return
        if key == 'space':
            app.space = True
            row, col = app.getCell(app, app.cx, app.cy)
            cell = app.board[row][col]
            if type(cell) == int: 
                if not app.noNeighboringMines(app, row, col):
                    return
                app.clearNeighbors(app, row, col)
            elif cell == 'mine':
                app.board[row][col] = True
            elif cell == 'flag':
                app.board[row][col] = False
            elif cell == False:
                app.board[row][col] = 'flag'
            elif cell == True:
                app.board[row][col] = 'mine'
        elif key == 'r':
            app.restart(app)
        elif key == 'e':
            app.difficulty = 'easy'
            app.restart(app)
        elif key == 'm':
            app.difficulty = 'medium'
            app.restart(app)
        elif key == 'h':
            app.difficulty = 'hard'
            app.restart(app) 
        
    def onKeyRelease(app, key):
        if key == 'space':
            app.space = False

    def getCell(app, x, y):
        col = x // app.cellWidth
        row = y //app.cellHeight
        return int(row), int(col)

    def checkMine(app, r, c):
        test = app.board[r][c]
        if type(test) == bool and test:
            app.gameOver = True
            app.timing = False
            return
        app.checkNeighbors(app, r, c, set())
        
    def checkNeighbors(app, r, c, seen):
        if (r >= len(app.board) or c >= len(app.board[0]) or 
                r < 0 or c < 0):
            return
        elif (r, c) in seen:
            return
        app.board[r][c] = app.countNeighbors(app, r, c)
        seen.add((r, c))
        if app.board[r][c] == None:
            app.checkNeighbors(app, r, c+1, seen)
            app.checkNeighbors(app, r+1, c, seen)
            app.checkNeighbors(app, r-1, c, seen)
            app.checkNeighbors(app, r, c-1, seen)
            app.checkNeighbors(app, r-1, c-1, seen)
            app.checkNeighbors(app, r+1, c+1, seen)
            app.checkNeighbors(app, r-1, c+1, seen)
            app.checkNeighbors(app, r+1, c-1, seen)
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
                    app.checkNeighbors(app, testRow, testCol, set())
                else:
                    app.board[testRow][testCol] = app.countNeighbors(app, testRow, testCol)
        
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

    def checkWin(app):
        count = 0
        for row in app.board:
            for v in row:
                if type(v) == bool or v == 'mine':
                    count += 1
        return count == app.numOfMines

    def setDifficulty(app):
        app.cellWidth = app.cellHeight = 30
        if app.difficulty == 'easy':
            app.numOfMines = 9
            app.rows = 9
            app.cols = 10
        elif app.difficulty == 'medium':
            app.numOfMines = 40
            app.rows = 16
            app.cols = 16
        elif app.difficulty == 'hard':
            app.numOfMines = 99
            app.rows = 16
            app.cols = 30
        
    def restart(app):
        app.setDifficulty(app)
        app.board = [[False for _ in range(app.cols)] for _ in range(app.rows)]
        app.width = app.cols * app.cellWidth
        app.height = app.rows * app.cellHeight

        app.space = False
        app.newBoard = True
        app.gameOver = False
        app.winner = False

   ################helpers###################

def generateField(r, c, numOfMines, firstClick):
        board = [[False for _ in range(c)] for _ in range(r)]
        mines = 0
        while mines < numOfMines:
            randR = random.randrange(0, r)
            randC = random.randrange(0, c)
            if (randR,randC) in firstClick:
                continue
            elif not board[randR][randC]:
                board[randR][randC] = True
                mines += 1
        return board

def surroundingFirstClick(firstCell):
    firstClick = set()
    row,col = firstCell
    for dRow in [-1, 0 ,1]:
        for dCol in [-1, 0, 1]:
            firstClick.add((row+dRow, col+dCol))
    return firstClick