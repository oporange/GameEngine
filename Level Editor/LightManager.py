import pygame, math, sys

path = sys.path[0].removesuffix("\\Level Editor")
sys.path.append(f"{path}/Scripts/")
from GUI import *
import GlobalInputManager

Lights = []

GlobalLightLevel = 30

class LightObject():

    def __init__(self, x, y, type):
        
        self.x = x
        self.y = y

        #Light types: 0 = point light, 1 = spot light

        self.intensity = 200
        self.type = type

        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

        self.selected = False

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.LeftClickFunc)

        self.ParamEditor = ParameterEditor(100,600,"Light")
        self.ParamEditor.AddParameter(Slider, self.IntensityChanged, 0.5)

    def update(self, LevelPos):

        self.rect = pygame.Rect(self.x - 5 + LevelPos[0], self.y - 5 +LevelPos[1], 10, 10)

        if self.selected:
            pygame.draw.rect(pygame.display.get_surface(), "red", self.rect)

            pygame.draw.circle(pygame.display.get_surface(), "green", (self.x + LevelPos[0], self.y + LevelPos[1]), self.intensity, 1)
            self.ParamEditor.update()
        else:
            pygame.draw.rect(pygame.display.get_surface(), "yellow", self.rect)

    def CalcLight(self, surf, startX, startY, lvlSurface):

        surface = surf
        ThisSurf = pygame.Surface((self.intensity * 2, self.intensity*2), pygame.SRCALPHA)

        if self.type == 0:
            for angle in range(0,1440):
                rad = math.radians(angle/4)

                for dist in range(self.intensity*2):
                    dist = dist/2
                    x = dist * math.cos(rad) + self.intensity
                    y = dist * math.sin(rad) + self.intensity

                    color = (0, 0, 0, 255 - 255 * (dist/self.intensity))

                    Px = x + self.x - self.intensity
                    Py = y + self.y - self.intensity

                    if lvlSurface.IsWrittenPixel(1, Px, Py):
                        break
                    else:

                        pygame.draw.rect(ThisSurf, color, pygame.Rect(x, y, 1, 1))

        surface.blit(ThisSurf, (self.x - startX, self.y - startY))

    def LeftClickFunc(self):
        if pygame.Rect.collidepoint(self.rect, pygame.mouse.get_pos()):
            self.selected = True
            for i in Lights:
                if i != self:
                    i.selected = False
            return True
        
    def IntensityChanged(self, value):

        self.intensity = round(400*value)

def CalcLights(levelDir, lvlSurface):

    progress = ProgressBar(len(Lights), "Calculating Lightmap")
    progress.update()
    pygame.display.update()

    def keyX(l):
        return l.x
    def keyY(l):
        return l.y
    def keyI(l):
        return l.intensity

    xList = Lights.copy()
    yList = Lights.copy()
    iList = Lights.copy()

    xList.sort(key = keyX)
    yList.sort(key = keyY)
    iList.sort(key = keyI)

    HighXList = xList[-1]
    LowXList = xList[0]

    HighYList = yList[-1]
    LowYList = yList[0]

    HightIntensity = iList[-1]
    
    LowX, LowY = 0,0
    HighX, HighY = 0,0

    for i in Lights:
        if i.x - i.intensity < LowX:
            LowX = i.x - i.intensity
        if i.y - i.intensity < LowY:
            LowY = i.y - i.intensity
            
        if i.x + i.intensity > HighX:
            HighX = i.x + i.intensity
        if i.y + i.intensity > HighY:
            HighY = i.y + i.intensity

    Lightmap = pygame.Surface((HighX - LowX, HighY - LowY), pygame.SRCALPHA)
    Lightmap.fill((0,0,0,0))
    
    print(LowX, LowY)

    print("Lightmap res", HighX - LowX, HighY - LowY)

    for i in Lights:
        print(i.x, i.y)
        i.CalcLight(Lightmap, LowXList.x, LowYList.y, lvlSurface)
        
        progress.add()
        progress.update()
        pygame.display.update()

    pygame.image.save(Lightmap, f"{levelDir}\\Lightmap.png")

    with open(f"{levelDir}\\Lightmap.txt", "w") as f:
        f.write(f"{LowXList.x - LowXList.intensity}x{LowYList.y-LowYList.intensity}")

    print("LightMap Calculated!")

