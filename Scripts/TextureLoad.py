import sys, pygame, os
from pathlib import Path
path = Path(__file__)

path = str(path).removesuffix("\Scripts\\TextureLoad.py")
GUIdir = f"{path}/GUI/"
TextureDir = f"{path}/Textures"
sys.path.append(f"{path}/GUI/")
sys.path.append(f"{path}/Textures/")

class Textures():
    Empty = pygame.Surface((32, 32))
    Empty.set_colorkey("black")
    class Walls():
        os.chdir(TextureDir)
        
        Red = pygame.image.load("Red.png").convert_alpha()
        Yellow = pygame.image.load("Yellow.png").convert_alpha()
        Blue = pygame.image.load("Blue.png").convert_alpha()
        Orange = pygame.image.load("Orange.png").convert_alpha()
        Lilac = pygame.image.load("Lilac.png").convert_alpha()
        Green = pygame.image.load("Green.png").convert_alpha()
        Black = pygame.image.load("Black.png").convert_alpha()

        Concrete = pygame.image.load("ConcreteWall.png").convert_alpha()
        
        List = [Red, Yellow, Blue, Orange, Lilac, Green]

    class Floors():
        os.chdir(TextureDir)

        Dirt = pygame.image.load("Dirt.png").convert_alpha()
        Gravel = pygame.image.load("Gravel.png").convert_alpha()
        Wood = pygame.image.load("WoodTile.png").convert_alpha()
        KitchenTile = pygame.image.load("KitchenTile.png").convert_alpha()
        Asphalt = pygame.image.load("Asphalt.png").convert_alpha()
        

        List = [Dirt, Gravel, Wood, KitchenTile, Asphalt]

        
    class UI():
        os.chdir(GUIdir)
        BlockIcon = pygame.image.load("block_icon.png").convert_alpha()
        FloorIcon = pygame.image.load("floor_icon.png").convert_alpha()
        LightIcon = pygame.image.load("light_icon.png").convert_alpha()
        



print("Textures Loaded!")