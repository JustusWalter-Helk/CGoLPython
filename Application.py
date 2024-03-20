from sdl2 import SDL_INIT_EVERYTHING, SDL_Init
from Window import *

import uuid

import time

from Renderer import *

import sdl2.ext

cellSize : int = 20
cellMargin : int = 5

 #Dont draw using GPU
factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

cells : list[Cell] = []

#Instead of calculating the neighbours each simulation step, we can precalculate them and safe them in a array
#To get the neighbours of a cell index this array at cellIndex * 8
precalculatedNeighbours : list[Cell] = []

#Util function
def getCellAtPosition(row : int, column : int):
    cell : Cell
    for cell in cells:
        if cell.cellinformation.row == row and cell.cellinformation.column == column:
            return cell
    dummyWorld = sdl2.ext.World()
    dummySprite = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE).from_color((2,2,2,2), size=(0,0))
    return Cell(dummyWorld, dummySprite, -100,-100, -100,-100)

def stepSimulation():
    startTime = time.time()
    cell : Cell
    #Update Neighbour counts
    for cell in cells:
        cellIndex = cells.index(cell)

        alive = 0
        
        neighbourIndices = range(cellIndex * 8, (cellIndex + 1) * 8)
        for neighbourIndex in neighbourIndices:
            neighbourCell = precalculatedNeighbours[neighbourIndex]
            if neighbourCell.cellinformation.enabled:
                alive += 1
        
        cell.cellinformation.aliveNeighbours = alive
        
    #cell.cellinformation.aliveNeighbours = left.cellinformation.enabled + up.cellinformation.enabled + right.cellinformation.enabled + down.cellinformation.enabled + leftUp.cellinformation.enabled + leftDown.cellinformation.enabled + rightDown.cellinformation.enabled + rightUp.cellinformation.enabled
    #Actually update Cell states
    for cell in cells:
        aliveCounter : int = cell.cellinformation.aliveNeighbours
        enabled : bool = cell.cellinformation.enabled

        if enabled and aliveCounter < 2: cell.cellinformation.enabled = False
        if enabled and (aliveCounter == 2 or aliveCounter == 3): cell.cellinformation.enabled = True
        if enabled and aliveCounter > 3: cell.cellinformation.enabled = False
        if enabled == False and aliveCounter == 3: cell.cellinformation.enabled = True

        color = (40,122,122,255)

        if enabled:
            color = (255,255,255,255)

        newSprite = factory.from_color(color, size=(cellSize, cellSize))
        cell.updateSprite(newSprite)
    print("Simulation Step took", time.time() - startTime, "seconds")

class Application:
    def __init__(self) -> None:
        self.running = False

    def Intitialize(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        self.mainWindow : Window = Window(WindowProps("Conways Game of Life", 800, 800))
        
    def Run(self):
        self.mainWindow.window.show()
        self.running = True

        world = sdl2.ext.World()

        self.spriteRenderer = self.mainWindow.renderer
        
        world.add_system(self.spriteRenderer)

        #Add cells to Game World
        numRows : int = int(self.mainWindow.window.size[1] / (cellSize + cellMargin))
        numColumns : int = int(self.mainWindow.window.size[0] / (cellSize + cellMargin))

        print("Number rows", numRows, "Number Columns", numColumns)
        
        for column in range(0, numColumns):
            for row in range(0, numRows):
                cellSprite = factory.from_color((40,122,122,255), size=(cellSize, cellSize))
                
                cell = Cell(world, cellSprite, row, column, (column * (cellSize + cellMargin)), (row * (cellSize + cellMargin)))
                
                cell.cellinformation.UUID = uuid.uuid4()

                cells.append(cell)

        currentIndex : int = 0
        for cell in cells:
            #Precalculating Neighbours
            row : int = cell.cellinformation.row
            column : int = cell.cellinformation.column

            left : Cell = getCellAtPosition(row - 1 ,column)
            up : Cell = getCellAtPosition(row, column + 1)
            right : Cell = getCellAtPosition(row + 1, column)
            down : Cell = getCellAtPosition(row, column - 1)

            leftUp : Cell = getCellAtPosition(row - 1, column + 1)
            leftDown : Cell = getCellAtPosition(row - 1, column - 1)
            rightUp : Cell = getCellAtPosition(row + 1, column + 1)
            rightDown : Cell = getCellAtPosition(row + 1, column - 1)

            precalculatedNeighbours.append(left)
            precalculatedNeighbours.append(up)
            precalculatedNeighbours.append(right)
            precalculatedNeighbours.append(down)

            precalculatedNeighbours.append(leftUp)
            precalculatedNeighbours.append(leftDown)
            precalculatedNeighbours.append(rightUp)
            precalculatedNeighbours.append(rightDown)

            currentIndex += 8

        print(precalculatedNeighbours[10].cellinformation.row)

        #Entering game loop
        while(self.running):
            events : list = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    self.running = False
                    break
                
                #Check for Mouse Press
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    mouseX, mouseY = event.button.x, event.button.y

                    cellColumn = mouseX // (cellSize + cellMargin)
                    cellRow = mouseY // (cellSize + cellMargin)

                    cell : Cell = getCellAtPosition(cellRow, cellColumn)

                    cell.cellinformation.enabled = True
                    newSprite = factory.from_color((255,255,255), size=(cellSize, cellSize))
                    cell.updateSprite(newSprite)
                elif event.button.button == sdl2.SDL_BUTTON_RIGHT:
                    mouseX, mouseY = event.button.x, event.button.y

                    cellColumn = mouseX // (cellSize + cellMargin)
                    cellRow = mouseY // (cellSize + cellMargin)

                    cell : Cell = getCellAtPosition(cellRow, cellColumn)

                    cell.cellinformation.enabled = False
                    newSprite = factory.from_color((40,122,122), size=(cellSize, cellSize))
                    cell.updateSprite(newSprite)

                #Check if F key is pressed
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_f:
                        stepSimulation()
            world.process()
            self.mainWindow.window.refresh()