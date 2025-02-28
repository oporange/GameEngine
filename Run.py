from Engine import *
import pygame, sys


texture = pygame.surface.Surface((32, 32))
texture.fill("red")


LevelData = Load(sys.path[0].removesuffix("Run.py") + "\\resources\\Levels\\test\\test.zip")
LevelSurface = LevelData[0]
LevelSurfaceOffset = LevelData[1]

class Player(Entity):
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        
        self.texture = texture
    
player = Player(300, 200, texture)

while True:
    
    GlobalInputManager.update()
    for event in pygame.event.get():
        if GlobalInputManager.GlobalInput(event) != 0:
            pass
    
    window.fill("black")

    window.window.blit(LevelSurface, (LevelSurfaceOffset[0]*32,LevelSurfaceOffset[1]*32))

    player.update()
    
    pygame.display.update()
        
        
    