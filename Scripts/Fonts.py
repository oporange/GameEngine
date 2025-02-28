import sys
from Imports import *

pygame.init()

from pathlib import Path
path = Path(__file__)

path = str(path).removesuffix("\Scripts\\Fonts.py")
sys.path.append(f"{path}/Fonts/")

KongText11 = pygame.freetype.Font(f"{path}\\Fonts\\kongtext.ttf", 11)
KongText9 = pygame.freetype.Font(f"{path}\\Fonts\\kongtext.ttf", 9)
KongText8 = pygame.freetype.Font(f"{path}\\Fonts\\kongtext.ttf", 8)