import pygame, sys, random, math, LightManager

path = sys.path[0].removesuffix("\\Level Editor")
sys.path.append(f"{path}/Scripts/")
import GlobalInputManager
import GlobalVars
import GUI

class Chunk():
    def __init__(self, x, y, lvl):
        # chunk size = 16x16 tiles, 512x512 pixels

        self.x = x
        self.y = y

        print(x,y)

        self.level = lvl

        self.surface = pygame.Surface((512, 512))
        self.surface.set_colorkey("black")

        self.Wallsurface = pygame.Surface((512, 512))
        self.Wallsurface.set_colorkey("black")

        self.Floorsurface = pygame.Surface((512, 512))
        self.Floorsurface.set_colorkey("black")

        self.Decalsurface = pygame.Surface((512, 512))
        self.Decalsurface.set_colorkey("black")

        self.surfaceOutline = pygame.Surface((512, 512))
        self.surfaceOutline.set_colorkey("black")

        self.boarderColor = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pygame.draw.rect(self.surfaceOutline, self.boarderColor, pygame.Rect(0, 0, 512, 512), 3)

    def update(self):
        if GlobalVars.ShowChunkOutlines:
            pygame.display.get_surface().blit(self.surfaceOutline, (self.x*32 + self.level.pos[0], self.y*32 + self.level.pos[1]))
        pygame.display.get_surface().blit(self.surface, (self.x*32 + self.level.pos[0], self.y*32 + self.level.pos[1]))

    def RenderToSurf(self, surf, pos, type):
        if type == 0:
            self.Wallsurface.blit(surf, (pos[0]-self.x*32, pos[1]-self.y*32))
            self.Floorsurface.blit(surf, (pos[0]-self.x*32, pos[1]-self.y*32))
            self.surface.blit(surf, (pos[0]-self.x*32, pos[1]-self.y*32))
        if type == 1:
            self.Wallsurface.blit(surf, (pos[0]-self.x*32, pos[1]-self.y*32))
            self.surface.blit(self.Wallsurface, (0,0))
        if type == 2:
            self.Floorsurface.blit(surf, (pos[0]-self.x*32, pos[1]-self.y*32))
            self.surface.blit(self.Floorsurface, (0,0))


class LevelSurface():
    def __init__(self, WindowSize, drawGhost):

        self.pos = (0,0)

        self.surface = pygame.Surface(WindowSize)
        self.surface.set_colorkey("black")

        self.Chuncks = []

        self.EmptySurf = pygame.Surface((32,32))

        self.drawGhost = drawGhost

        self.LClick = False
        self.Rclick = False
        self.Mclick = False

        self.MclickStartPos = (0,0)
        self.Addpos = (0,0)

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, -1, self.LClickFunc)
        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickReleaseCmds, -1, self.LUnclickFunc)

        GlobalInputManager.AddCMD(GlobalInputManager.RightClickCmds, -1, self.RClickFunc)
        GlobalInputManager.AddCMD(GlobalInputManager.RightClickReleaseCmds, -1, self.RUnclickFunc)

        GlobalInputManager.AddCMD(GlobalInputManager.MiddleClickCmds, -1, self.MClickFunc)
        GlobalInputManager.AddCMD(GlobalInputManager.MiddleClickReleaseCmds, -1, self.MUnclickFunc)

    def update(self, mousePos, dropdowns, gridScale, drawType):
        mousePos = (round(((pygame.mouse.get_pos()[0] - self.pos[0]%32) - (gridScale/2)) / gridScale) * gridScale  + self.pos[0]%32,
                    round(((pygame.mouse.get_pos()[1] - self.pos[1]%32) - (gridScale/2)) / gridScale) * gridScale  + self.pos[1]%32)
        
        draw = False
        openDropDown = False
        for i in dropdowns:
            if i.ActiveVar() == i.WhenEquals:
                draw = True
                openDropDown = i
                break

        if draw:
            self.drawGhost.update(mousePos, (gridScale, gridScale))

        if (self.LClick or self.Rclick) and draw:
            if drawType == 4:
                if GlobalInputManager.LclickFrame:
                    LightManager.Lights.append(LightManager.LightObject(pygame.mouse.get_pos()[0] - self.pos[0], pygame.mouse.get_pos()[1] - self.pos[1], openDropDown.Selected().reference))
            for i in self.Chuncks:
                if ((i.x*32 <= pygame.mouse.get_pos()[0] - self.pos[0] and i.x*32 + 512 >= pygame.mouse.get_pos()[0] - self.pos[0]) and 
                    (i.y*32 <= pygame.mouse.get_pos()[1] - self.pos[1] and i.y*32 + 512 >= pygame.mouse.get_pos()[1] - self.pos[1])):
                    if self.LClick:
                        i.RenderToSurf(openDropDown.Selected().reference, (mousePos[0] - self.pos[0], (mousePos[1] - self.pos[1])), drawType)
                    if self.Rclick:
                        i.RenderToSurf(self.EmptySurf, (mousePos[0] - self.pos[0], (mousePos[1] - self.pos[1])), 0)
                    break
            else:
                x, y = math.floor((mousePos[0] - self.pos[0]) / 512) * 16, math.floor((mousePos[1] - self.pos[1]) / 512) * 16
                if not any(i.x == x and i.y == y for i in self.Chuncks):
                    self.Chuncks.append(Chunk(x, y, self))

        for i in self.Chuncks:
            i.update()

        pygame.display.get_surface().blit(self.surface, (0,0))

        if self.Mclick:
                self.pos = (self.Addpos[0] + pygame.mouse.get_pos()[0] - self.MclickStartPos[0], self.Addpos[1] + pygame.mouse.get_pos()[1] - self.MclickStartPos[1])

    def IsWrittenPixel(self, surfType, x, y):

        for i in self.Chuncks:
            if ((i.x*32 <= x and i.x*32 + 512 >= x) and 
                (i.y*32 <= x and i.y*32 + 512 >= y)):

                if surfType == 1:
                    try:
                        if i.Wallsurface.get_at((round(x - i.x * 32), round(y - i.y * 32))) != (0,0,0):
                            return i.Wallsurface.get_at((round(x - i.x * 32), round(y - i.y * 32)))
                    except:
                        pass

        else:
            return False


    def LClickFunc(self):
        self.LClick = True
    def LUnclickFunc(self):
        self.LClick = False

    def RClickFunc(self):
        self.Rclick = True
    def RUnclickFunc(self):
        self.Rclick = False

    def MClickFunc(self):
        self.Mclick = True
        GUI.Cursor.ChangeCursor(6)
        self.MclickStartPos = pygame.mouse.get_pos()
    def MUnclickFunc(self):
        self.Mclick = False
        self.pos = (self.Addpos[0] + pygame.mouse.get_pos()[0] - self.MclickStartPos[0], self.Addpos[1] + pygame.mouse.get_pos()[1] - self.MclickStartPos[1])
        self.Addpos = self.pos
        GUI.Cursor.ChangeCursor(0)

    def ReturnChunks(self):
        return self.Chuncks