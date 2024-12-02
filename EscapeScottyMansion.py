from cmu_graphics import *
from PIL import Image
import os, pathlib
import Graphic
import Maze
import Minefield

def onAppStart(app):
    app.cx = 0
    app.cy = 0
    app.stepsPerSecond = 10
    app.steps = 0

########################################################### INTRO ############################################################
##############################################################################################################################

def intro_onScreenActivate(app):
    app.lightning = False
    app.lightningSound = loadSound('loud-thunder.mp3')

def intro_redrawAll(app):
    #load photo urls:
    #house = Image.open("haunted_mansion.png")
    lightningURL = ('https://t3.ftcdn.net/jpg/05/04/77/04/360_F_504770428_Zql2YdgeC1s5uWmDWTZbb0fLUdTWtai9.jpg')
    # doorSpriteSheet = Graphic.Sprite("https://i.imgur.com/pHUZbF4.png")
    # doorGraphic = Graphic.crop(doorGraphic, 7)

    drawRect(0, 0, app.width, app.height)
    drawLabel("Escape Scotty Mansion!!!", app.width//2, app.height//2, fill = 'red', size = app.width//13)
    drawImage(lightningURL, 0, 0, width = app.width, height = app.height, visible = app.lightning)

def intro_onMouseMove(app, mouseX, mouseY):
    app.cx = mouseX
    app.cy = mouseY

def intro_onStep(app):
    app.steps += 1
    if app.steps == 30:
        app.lightning = True
        Sound.play(app.lightningSound, restart=False, loop=False)
    if app.steps == 40:
        app.lightning = False

######################################################### SETUP ############################################################
############################################################################################################################
def setup_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='red')
    

######################################################### BOARD ############################################################
############################################################################################################################
def board_onScreenActivate(app):
    mazeBoard = Maze.Maze(app.rows, app.cols)
    mineBoard = Minefield.Minefield()

def board_redrawAll(app):
    drawBoard(app)  
    if app.gameOver: app.drawGameOver(app)

    def drawBoard(app):
        for row in range(app.rows):
            for col in range(app.cols):
                cellLeft = col * app.cellWidth
                cellTop = row * app.cellHeight
                cell = app.board[row][col]

                if type(cell) == int or cell == None:
                    cellColor = 'gray'
                elif app.gameOver and cell:
                    cellColor = 'darkRed'
                else:
                    cellColor = 'darkGray'
                    
                drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight, 
                fill = cellColor, border = 'gray', borderWidth = 0.5)
                
                if cell == 'flag' or cell == 'mine':
                    drawCircle(cellLeft + app.cellWidth/2, cellTop + app.cellHeight/2, app.cellWidth/4,
                        fill = 'red')
                elif type(cell) != bool:
                    label = cell if cell != None else ''
                    drawLabel(label, cellLeft + app.cellWidth/2, cellTop + app.cellHeight/2,
                    font = 'orbitron', size = 16)
        
    def drawGameOver(app):
        drawLabel('GAME OVER :(', app.width/2, app.height/2, size = 40, 
            font = 'orbitron', fill = 'red', bold = True)

######################################################### HELPERS ###########################################################
#############################################################################################################################
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)

###################################################### KEY EVENTS #########################################################
#############################################################################################################################


runAppWithScreens(initialScreen='intro')