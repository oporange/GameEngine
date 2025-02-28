import pygame, sys, os, zipfile

def Load(LevelDirectory):

    with zipfile.ZipFile(LevelDirectory, "r") as level:
        
        LevelSurface = pygame.image.load(level.open("LevelSurface.png"))

        with level.open("LevelSurfaceOffset.txt") as file:
            LevelSurfaceOffset = file.read().split()
            print(LevelSurfaceOffset)

            try:
                x = int(LevelSurfaceOffset[0])
            except:
                x = 0
            try:
                y = int(LevelSurfaceOffset[1])
            except:
                y = 0

            LevelSurfaceOffset = (x,y)

    return [LevelSurface, LevelSurfaceOffset]