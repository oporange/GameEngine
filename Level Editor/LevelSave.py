import pygame, os

def SaveLevel(Directory, chunksList):
    GlobalFilePath = __file__.removesuffix("\\Level Editor\\LevelSave.py")+"\\Levels" + "\\" + Directory + "\\"
    chunksList = chunksList()

    chunksFolder = GlobalFilePath + "Chunks"

    os.chdir(chunksFolder)

    for i in chunksList:
        os.chdir(chunksFolder)
        dirName = f"{i.x}x{i.y}"
        try:
            os.mkdir(dirName)
        except:
            print("already exists")

        os.chdir(dirName)

        pygame.image.save(i.Wallsurface, f"Walls.png")
        pygame.image.save(i.Floorsurface, f"Floors.png")
