import sys

path = sys.path[0].removesuffix("\\Level Editor")
sys.path.append(f"{path}/Scripts/")
from GUI import *
from TextureLoad import *


def DropdownCreateTextureList(TexList):

    List = []

    for i in TexList:
        List.append(GuiItem(i, i))

    return List