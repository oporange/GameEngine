import pygame, os
import LoadLevelScreen
import sys
from PlaceTextures import *
from SelectedManager import *
import LevelSave, LightManager, LevelExport

path = sys.path[0].removesuffix("\\Level Editor")
sys.path.append(f"{path}/Scripts/")
from GlobalInputManager import *
from GUI import *
from Window import *
from Fonts import *
import GlobalVars

pygame.init()

def LoadLevel(LevelDir, LvlSurf):
    LevelDirectory = path+"\\Levels" + "\\" + LevelDir + "\\"
    os.chdir(LevelDirectory)
    
    with open("Level.lvl", "r") as LevelSave:
        print(LevelSave.read())

    for i in os.listdir(f"{LevelDirectory}\\Chunks\\"):
        directory = f"{LevelDirectory}\\Chunks\\{i}"
        chunkPos = i.split("x")
        print(chunkPos)
        chunk = LevelManager.Chunk(int(chunkPos[0]), int(chunkPos[1]), levelSurface)

        chunk.Wallsurface.blit(pygame.image.load(f"{directory}\\Walls.png").convert_alpha(), (0,0))
        chunk.Floorsurface.blit(pygame.image.load(f"{directory}\\Floors.png").convert_alpha(), (0,0))

        chunk.surface.blit(chunk.Floorsurface, (0,0))
        chunk.surface.blit(chunk.Wallsurface, (0,0))

        LvlSurf.Chuncks.append(chunk)

    LvlSurf.update((0, 0), [], 32, lambda: 0)
    pygame.display.update()

    return LevelDirectory
    
    
LevelToLoad = LoadLevelScreen.Run() # calls Level Select screen for loading a level to edit - script returns name of directory chosen to edit

window = screen()
window.SetTitle("LevelEditor - " + LevelToLoad)

from TextureLoad import *
import LevelManager, GUI_dropdown_lists

grid = Grid(32, (window.ScrW,window.ScrH))

DrawGhost = SelectionArea("purple", window.window)
levelSurface = LevelManager.LevelSurface((window.ScrW, window.ScrH), DrawGhost)

LevelDirectory = LoadLevel(LevelToLoad, levelSurface)

# Code that defines the Tool/Menu bar on the gui
menu = MenuBar(0)
menu.Add("File")
menu.Add("Edit")
menu.Add("View")
menu.Add("Light")
menu.Add("Run")

menu.AddChild("File", "Exit", quit, False)
menu.AddChild("File", "Save", lambda : LevelSave.SaveLevel(LevelToLoad, levelSurface.ReturnChunks), False)
menu.AddChild("File", "Export", lambda: LevelExport.Export(LevelDirectory, levelSurface, LevelToLoad), False)

menu.AddChild("Edit", "Size", lambda: print("Size Change Called"), False)
menu.AddChild("Edit", "Texture", lambda: print("Texture Change Called"), False)

menu.AddChild("View", "Show Grid", lambda: grid.Show(), pygame.K_g)
menu.AddChild("View", "Grid +", lambda: grid.Size(2), pygame.K_y)
menu.AddChild("View", "Grid -", lambda: grid.Size(0.5), pygame.K_h)
menu.AddChild("View", "Show Chunk OutLines", lambda: GlobalVars.ShowChunkOutlinesFunc(), pygame.K_c)

menu.AddChild("Light", "Calculate Lightmap", lambda: LightManager.CalcLights(LevelDirectory, levelSurface), False)

menu.AddChild("Run", "Run", lambda: print("Run Called"), False)
menu.AddChild("Run", "Debug", lambda: print("Debug Called"), False)
menu.AddChild("Run", "Debug & Log", lambda: print("Debug & Log Called"), False)
#------------------------------------------------------------------------------

ToolSwitchExclusive = ExclusiveSwitchManager()
ToolGroup = []
ToolGroup.append(Switch(window.ScrW - 24, 20, Textures.UI.BlockIcon, ToolSwitchExclusive, lambda: ChangeSelectedTool("Wall"), lambda: ChangeSelectedTool("")))
ToolGroup.append(Switch(window.ScrW - 24, 44, Textures.UI.FloorIcon, ToolSwitchExclusive, lambda: ChangeSelectedTool("Floor"), lambda: ChangeSelectedTool("")))
ToolGroup.append(Switch(window.ScrW - 24, 92, Textures.UI.LightIcon, ToolSwitchExclusive, lambda: ChangeSelectedTool("Light"), lambda: ChangeSelectedTool("")))

DropDowns = []
DropDowns.append(DropdownUI(100, 400, "Wall Textures",[GuiItem(Textures.Walls.Red, Textures.Walls.Red),
                                 GuiItem(Textures.Walls.Yellow, Textures.Walls.Yellow),
                                 GuiItem(Textures.Walls.Blue, Textures.Walls.Blue),
                                 GuiItem(Textures.Walls.Orange, Textures.Walls.Orange),
                                 GuiItem(Textures.Walls.Lilac, Textures.Walls.Lilac),
                                 GuiItem(Textures.Walls.Green, Textures.Walls.Green),
                                 GuiItem(Textures.Walls.Concrete, Textures.Walls.Concrete)], lambda: ToolGroup[0].Toggled, True, SelectedWallTexture))

DropDowns.append(DropdownUI(100,400,"Floor Textures", GUI_dropdown_lists.DropdownCreateTextureList(Textures.Floors.List), lambda: ToolGroup[1].Toggled, True, SelectedWallTexture))

DropDowns.append(DropdownUI(100,400,"Lights", [GuiItem(Textures.Walls.Black, 0)], lambda: ToolGroup[2].Toggled, True, SelectedWallTexture))

Param = ParameterEditor(100, 200, "Test")
Param.AddParameter(Slider, Param.x, 0)

while True:
    x, y = pygame.mouse.get_pos()
    RoundedX = round((x- grid.size/2)/grid.size)*grid.size
    RoundedY = round((y- grid.size/2)/grid.size)*grid.size

    GlobalInputManager.update()

    for event in pygame.event.get():
        if GlobalInput(event) != 0:
            pass
        
    window.fill("black")
        
    grid.update((levelSurface.pos[0]%32, levelSurface.pos[1]%32))
    
    levelSurface.update((RoundedX, RoundedY), DropDowns, grid.size, returnSelectedTool())

    for i in LightManager.Lights:
        i.update(levelSurface.pos)

    menu.update()

    for i in ToolGroup:
        i.update()
        
    for i in DropDowns:
        i.update()

    #Param.update()
        
    

    pygame.display.update()
        