import sdl2.ext

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    #ECS?
    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(22,46,37,255))
        super(SoftwareRenderer, self).render(components)

class Cell(sdl2.ext.Entity):

    def __init__(self,world,sprite, row, column,posx=100, posy=100):
        self.sprite = sprite
        self.sprite.position = posx,posy
        self.cellinformation = CellInformation(row,column)

    def updateSprite(self, sprite):
        posX, posY = self.sprite.position
        self.sprite = sprite
        self.sprite.position = posX,posY

class CellInformation(object):
    def __init__(self, row , column):
        super(CellInformation, self).__init__()
        self.row = row
        self.column = column
        self.enabled = False
        self.aliveNeighbours = 0

        self.UUID = 0