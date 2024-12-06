from cmu_graphics import *
import time
import Graphic
import Player
import Maze
import Minesweeper

def onAppStart(app):
    app.width = 900
    app.height = 600
    app.cellWidth = app.cellHeight = 3
    app.stepsPerSecond = 10
    app.steps = 0

    ### colors ###
    app.red = rgb(106,32,32)
    app.darkRed = rgb(53, 16, 16)
    app.brown = rgb(47,14,7)
    app.yellow = rgb(255,211,0)
    app.gray = rgb(97,112,115)
    app.orange = rgb(236,78,32) 
    app.navy = rgb(0,20,39)

def drawInstructionsButton(app):
    drawCircle(app.width-(app.width//11), app.height-(app.width//11), app.width//22, fill = app.brown, 
            border = app.yellow, borderWidth = 3)
    drawLabel('?', app.width-(app.width//11), app.height-(app.width//11), size = app.width//12, fill = app.yellow, 
               font = 'Jim NightShade') 
    #if (Player.distance(mouseX, mouseY, app.width-(app.width//11), app.height-(app.width//11)) < app.width//22): 
        # setActiveScreen('instructions')

def drawBackButton(app):
    drawLabel('<', (app.width//11), (19*app.height//22), size = app.width//6,
              font = 'Jim NightShade', fill = app.yellow)
    # if (app.width//22 < mouseX < 3*app.width//22 and 19*app.height//22 < mouseY < 21*app.height//22):
    #     setActiveScreen(app.prevScreen)

def lightningFX(app):
    pass
########################################################### INTRO ############################################################
##############################################################################################################################


def intro_onScreenActivate(app):
    app.player = Player.Player()
    app.storyMode = False
    app.introTransition = False

def intro_redrawAll(app):
    drawRect(0, 0, app.width, app.height)
    drawLabel("Escape Scotty Mines", app.width//2, app.height//4, fill = app.yellow, size = app.width//13, 
              font = 'Jim Nightshade', align = 'top')
    intro_drawButton(app, 'Story Mode', app.width//9, 5*app.height//8, app.width//3, app.height//8)
    intro_drawButton(app, 'Free Play', 5*app.width//9, 5*app.height//8, app.width//3, app.height//8)
    if app.introTransition:
        if app.steps <= 20:
            drawRect(0, 0, app.width, app.height, opacity = (app.steps)*5)
        else: 
            drawRect(0, 0, app.width, app.height)
            setActiveScreen('storyPlot')

def intro_drawButton(app, text, left, top, width, height):
    drawRect(left, top, width, height, fill = app.red, border = app.yellow)
    drawLabel(text, left + width//2, top + height//2, size = width//10, font = 'Jim Nightshade', 
              fill = app.yellow)

def intro_onMouseMove(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY

def intro_onMousePress(app, mouseX, mouseY):
    app.prevScreen = 'intro'
    if (app.width//9 <= mouseX <= 4*app.width//9 and
            5*app.height//8 <= mouseY <= 3*app.height//4): 
        intro_setStoryMode(app)
    elif (5*app.width//9 <= mouseX <= 8*app.width//9 and
            5*app.height//8 <= mouseY <= 3*app.height//4):
       setActiveScreen('setup')

def intro_setStoryMode(app):
    app.storyMode = True
    if app.player.playerBoard == None:
        app.difficulty = 1
        app.steps = 0
        app.introTransition = True
    else: setActiveScreen('storyLevelPass')
    
def intro_onStep(app):
    app.steps += 1


def instructions_redrawAll(app):
    controls = (['Controls:',
    '   - Click on a square to reveal it',
    '   - Press space bar while hovering over a square to flag',
    '      it or reveal its adjacent squares', 
    '   - Use arrow keys (up, down, right left) to move the player',
    '   - Player can deactivate flagged mines by touching them',
    '   - Find the highlighted maze exit to win!',
    '   - Press r to restart'])
    drawRect(0, 0, app.width, app.height, fill = app.red)
    for i in range(len(controls)):
        drawLabel(controls[i], app.width//11, (1+i)*app.height//10, size = app.width//25,
                  align = 'left', font = 'Jim NightShade', fill = app.yellow)
    drawBackButton(app)

def instructions_onMousePress(app, mouseX, mouseY):
    if (app.width//22 < mouseX < 3*app.width//22 and 19*app.height//22 < mouseY < 21*app.height//22):
        setActiveScreen(app.prevScreen)


def setup_onScreenActivate(app):
    app.player = Player.player()
    app.difficulty = 0

def setup_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill=app.red)
    drawLabel('Choose your difficulty level:', app.width//2, app.height//2, size = app.width//16,
              font = 'Jim Nightshade', fill = app.yellow)
    drawLabel(f'{app.difficulty}', app.width//2, 2*app.height//3, size = app.width//20,
              font = 'Jim Nightshade', fill = app.yellow)
    drawLabel('Click here to continue', app.width//2, 3*app.height//4, size = app.width//16,
              font = 'Jim Nightshade', fill = app.yellow)
    drawBackButton(app)
    drawInstructionsButton(app)

def setup_onMousePress(app, x, y):
    if (Player.distance(x, y, app.width-(app.width//11), app.height-(app.width//11)) < app.width//22): 
        setActiveScreen('instructions')
    elif (app.width//22 < x < 3*app.width//22 and 19*app.height//22 < y < 21*app.height//22):
       setActiveScreen(app.prevScreen)
    else: setActiveScreen('board')


######################################################### STORY MODE #######################################################
############################################################################################################################

def storyPlot_onStep(app):
    app.steps += 1
    if app.steps <= 60:
        app.storyText = "You are a worker in Scotty Mines"
    elif app.steps <= 80:
        app.storyText = "It is a dangerous profession..."
    elif app.steps <= 100:
        app.storyText = "...but your heart is in the work."
    elif app.steps <= 140:
        app.storyText = ("One day, a terrible storm traps you", "deep within the hazardous tunnels")
    else:
        app.storyText = "Will you escape?"

def storyPlot_onMousePress(app, mouseX, mouseY):
    if (Player.distance(mouseX, mouseY, app.width-(app.width//11), app.height-(app.width//11)) < app.width//22): 
        setActiveScreen('instructions')
    elif (app.width//3 <= mouseX <= 2*app.width//3 and 13*app.height//16 <= mouseY <= 15*app.height//16):
        setActiveScreen('storyLevelPass')
    elif (app.width//22 < mouseX < 3*app.width//22 and 19*app.height//22 < mouseY < 21*app.height//22):
        setActiveScreen('intro')

def storyPlot_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = app.red)
    drawStoryText(app, app.storyText, app.width//24, app.height//10, 11*app.width//12, 5*app.height//8)
    drawBackButton(app)
    drawInstructionsButton(app)
    if app.steps <= 40:
        drawRect(0, 0, app.width, app.height, opacity = (40-app.steps)*5)
    if app.steps == 150:
        lightningFX(app)
    if app.steps >= 170:
        intro_drawButton(app, 'Continue', app.width//3, 13*app.height//16, app.width//3, app.height//8)

def drawStoryText(app, text, left, top, width, height):
    drawRect(left, top, width, height, fill = 'black', border = app.brown, opacity = 50)
    if type(text)==tuple:
        drawLabel(text[0], left + width/2, top + 7*height/16, size = width//20, font = 'Jim Nightshade', fill = app.yellow)
        drawLabel(text[1], left + width/2, top + 9*height/16, size = width//20, font = 'Jim Nightshade', fill = app.yellow)
    else: drawLabel(text, left + width/2, top + height/2, size = width//20, font = 'Jim Nightshade', fill = app.yellow)

def storyLevelPass_onScreenActivate(app):
    app.steps = 0
    app.levelUp = True

def storyLevelPass_onStep(app):
    app.steps += 1
    if app.steps == 20:
        app.levelUp = True
        setActiveScreen('board')

def storyLevelPass_redrawAll(app):
    drawRect(0,0,app.width,app.height)
    drawLabel(f'Level {app.difficulty}', app.width//2, app.height//2, 
              size = app.width//10, font = 'Jim Nightshade', fill = app.yellow)

def storyEnd_onScreenActivate(app):
    app.steps = 0

def storyEnd_onStep(app):
    app.steps += 1

def storyEnd_redrawAll(app):
    message = 'Congrats, you win!' if app.winner else 'You died in the mines.'
    backgroundFill = app.red if app.winner else app.navy
    drawRect(0,0,app.width,app.height, fill = app.red)
    drawLabel(message, app.width//2, app.height//2, font = 'Jim NightShade', 
              size = app.width//15, fill = app.yellow)
    if app.steps >= 20:
        drawLabel('Click to play again', app.width//2, 2*app.height//3, 
                font = 'Jim NightShade', size = app.width//20, fill = app.yellow)
    
def storyEnd_onMousePress(app):
    if app.steps >= 20:
        setActiveScreen('intro')


######################################################### BOARD ############################################################
############################################################################################################################


def board_onScreenActivate(app):
    app.cellWidth = app.cellHeight = 30
    app.deactivateFlagColorList = [app.orange, app.red]
    if app.player.playerBoard == None or (app.levelUp and app.storyMode):
        app.player.newGame()
        board_restart(app)

def board_onStep(app):
    app.steps += 1
    app.time = app.steps//app.stepsPerSecond
    if app.player.deactivating:
        #alternating colors
        app.deactivateFlagColor = app.deactivateFlagColorList[(app.steps%2)]
        if app.time == (app.startTime + 3):
            board_deactivateMine(app)

def board_restart(app):
    if app.player.lives == 0: setActiveScreen('end')
    
    board_setBoardSpecs(app)
    app.mazeBoard = Maze.Maze(app.rows, app.cols)
    app.mineBoard = Minesweeper.Minefield(app.rows, app.cols, app.numOfMines)
    app.player.playerBoard = app.playerBoard = Player.PlayerBoard(app.mineBoard.board, app.mazeBoard.mazeLines)
    app.player.newGame()

    app.boardWidth = app.cols * app.cellWidth
    app.boardHeight = app.rows * app.cellHeight
    app.boardLeft = app.width//2 - app.boardWidth//2
    app.boardTop = app.height//2 - app.boardHeight//2
    
    app.space = app.levelUp = False
    app.newBoard = True
    app.gameOver = app.winner = False

def board_onMouseMove(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY
    if app.newBoard:
        app.player.x, app.player.y = mouseX, mouseY
    app.mouseRow, app.mouseCol = board_getCell(app, mouseX, mouseY)

def board_onMousePress(app, mouseX, mouseY):
    if (Player.distance(mouseX, mouseY, app.width-(app.width//11), app.height-(app.width//11)) < app.width//22): 
        app.prevScreen = 'board'
        setActiveScreen('instructions')
    elif (app.width//22 < mouseX < 3*app.width//22 and 19*app.height//22 < mouseY < 21*app.height//22):
         setActiveScreen('intro')
    elif board_isBoard(app, mouseX, mouseY):
        #restart after loss or win
        if app.gameOver:
            board_restart(app)
            return
        if app.winner:
            app.difficulty += app.storyMode
            setActiveScreen('storyLevelPass')
            return
    #play minesweeper
        if app.space: return

        row, col = board_getCell(app, mouseX, mouseY)

        if app.newBoard: 
            app.player.currC, app.player.currR = col, row
            app.mineBoard.generateField(row, col)
            app.newBoard = False

        cell = app.mineBoard.board[row][col]
        if cell == 'mine' or cell == 'flag' or type(cell) == int: return
        elif type(cell) == bool and cell: 
            app.gameOver = True
            app.player.lives -= 1
            return
        else: app.mineBoard.checkNeighbors(row, col, set())
        app.playerBoard.update(app.mineBoard.board)

def board_onKeyPress(app, key):
    if (app.player.deactivating or app.winner or app.gameOver): return

    if key == 'space':
        app.space = True
        app.mineBoard.flag(app.mouseRow, app.mouseCol)
        app.playerBoard.update(app.mineBoard.board)
    elif key == 'r':
        board_restart(app)
    elif key in ['up', 'down', 'left', 'right']:
        app.player.move(key)
        if app.player.lives == 0:
            if app.storyMode: setActiveScreen('end')
            else: setActiveScreen('setup')
        elif app.player.deactivating:
            app.startTime = app.time
        board_checkWin(app, key)

def board_onKeyRelease(app, key):
    if key == 'space':
        app.space = False

###draw###
def board_redrawAll(app):
    drawRect(0, 0, app.width, app.height)
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, fill = app.brown, border = app.yellow)
    drawBackButton(app)
    drawInstructionsButton(app)
    board_drawMaze(app)
    board_drawMineBoard(app)
    if app.player.x != None: board_drawPlayer(app)
    if app.gameOver or app.winner:
        board_drawMessage(app)

def board_drawMaze(app):
    for row, col, direction in app.mazeBoard.mazeLines:
        board_drawMazeLine(app, row, col, direction, app.yellow)
    winR, winC, winD = app.mazeBoard.win
    if (app.mineBoard.board[winR][winC] == None or type(app.mineBoard.board[winR][winC]) == int): 
        board_drawMazeLine(app, winR, winC, winD, 'red')

def board_drawMazeLine(app, row, col, direction, color):
    dX = dY = 0
    bLeft, bTop = app.boardLeft, app.boardTop
    cWidth, cHeight = app.cellWidth, app.cellHeight
    if direction == 'right': 
        dY = 1
        startX = bLeft + cWidth * (col+1)
        startY = bTop + cHeight * row
    elif direction == 'left':
        dY = 1
        startX = bLeft + cWidth * col
        startY = bTop + cWidth * row
    elif direction == 'down':
        dX = 1
        startX = bLeft + cWidth * col 
        startY = bTop + cHeight * (row+1)
    elif direction == 'up':
        dX = 1
        startX = bLeft + cWidth * col 
        startY = bTop + cHeight * row
    drawLine(startX, startY, startX + cWidth * dX, startY + cHeight * dY, fill = color)

def board_drawMineBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            cellLeft = col * app.cellWidth + app.boardLeft
            cellTop = row * app.cellHeight + app.boardTop
            cell = app.mineBoard.board[row][col]
            
            flagColor = app.orange
            cellColor = 'gray'
            if ((app.gameOver and cell) or 
                   (app.player.injury and app.player.deactivating == row,col)):
                cellColor = app.red
            elif (app.player.deactivating == row,col): flagColor = app.deactivateFlagColor

            if type(cell) != int and cell != None:
                drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight, 
                    fill = cellColor, border = app.gray, borderWidth = 0.5)
            
            if cell == 'flag' or cell == 'mine':
                drawCircle(cellLeft + app.cellWidth//2, cellTop + app.cellHeight//2, 
                           app.cellWidth//4, fill = flagColor)
            
            elif type(cell) != bool:
                label = cell if cell != None else ''
                drawLabel(label, cellLeft + app.cellWidth//2, cellTop + app.cellHeight//2,
                font = 'Futura', size = 17, fill = app.yellow)

def board_drawPlayer(app):
    if app.player.currC != None:
        cellLeft = app.boardLeft + app.player.currC * app.cellWidth
        cellTop = app.boardTop + app.player.currR * app.cellWidth
        drawCircle(cellLeft + app.cellWidth//2, cellTop + app.cellWidth//2, 5)
    elif board_isBoard(app, app.cx, app.cy):
        drawCircle(app.player.x, app.player.y, 5)
    drawLives = ['<3']*app.player.lives
    drawLabel(f'Lives: {drawLives}', app.width//20, app.height//10, size = app.width//27,
              align = 'left', font = 'Jim Nightshade', fill = app.yellow)
    drawLabel(f'Mines Left: {app.numOfMines}', app.width//20, 2*app.height//10, size = app.width//27,
              align = 'left', font = 'Jim Nightshade', fill = app.yellow)

def board_drawMessage(app):
    message = 'Try again...' if app.gameOver else 'You did it!'
    drawLabel(message, app.width//2, 9*app.height//10, size = app.width//20,
              font = 'Jim Nightshade', fill = app.yellow)

###help###
def board_getCell(app, x, y):
    col = (x-app.boardLeft) // app.cellWidth
    row = (y-app.boardTop) //app.cellHeight
    return int(row), int(col)

def board_isBoard(app, x, y):
    return ((app.boardLeft < x < app.boardLeft+app.boardWidth) and 
            (app.boardTop < y < app.boardTop+app.boardHeight))

def board_setBoardSpecs(app):
    if app.difficulty == 1:
        app.numOfMines = 9
        app.rows = 9
        app.cols = 10
    elif app.difficulty == 2:
        app.numOfMines = 40
        app.rows = 16
        app.cols = 16
    elif app.difficulty == 3:
        app.numOfMines = 99
        app.rows = 16
        app.cols = 30

def board_deactivateMine(app):
    row, col = app.player.deactivating
    app.mineBoard.board[row][col] = None
    app.mineBoard.checkNeighbors(row, col, set())
    app.playerBoard.update(app.mineBoard.board)
    app.numOfMines -= 1
    app.player.injury = app.player.deactivating = False
        

def board_checkWin(app, key):
    app.winner = ((app.player.currR == app.mazeBoard.win[0]) and 
                  (app.player.currC == app.mazeBoard.win[1]) and
                  (key == app.mazeBoard.win[2]))
    if app.storyMode and app.difficulty == 3:
        setActiveScreen('end')

#############################################################################################################################
#############################################################################################################################

runAppWithScreens(initialScreen='intro')