import pygame, math, LightManager, sys, os, shutil

path = sys.path[0].removesuffix("\\Level Editor")
sys.path.append(f"{path}/Scripts/")
from GUI import *

def Clamp(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    else:
        return val

def Export(dir, Lvl, LevelName):
        
    progress = ProgressBar(len(Lvl.Chuncks), "Exporting Chuncks")
    progress.update()
    pygame.display.update()
    
    def keyX(l):
        return l.x
    def keyY(l):
        return l.y

    xList = Lvl.Chuncks.copy()
    yList = Lvl.Chuncks.copy()

    xList.sort(key = keyX)
    yList.sort(key = keyY)

    HighX = xList[-1]
    LowX = xList[0]

    HighY = yList[-1]
    LowY = yList[0]

    FinalStaticSurface = pygame.Surface(((HighX.x - LowX.x) * 32 + 512, (HighY.y - LowY.y) * 32 + 512), pygame.SRCALPHA)
    LightSurface = FinalStaticSurface.copy()
    StaticSurface = FinalStaticSurface.copy()

    with open(f"{dir}\\Lightmap.txt") as f:
        offset = f.read()
        x, y = offset.split("x")

        LightSurface.blit(pygame.image.load(f"{dir}\\Lightmap.png"), (int(x) - LowX.x * 32, int(y) - LowY.y*32))

    for i in Lvl.Chuncks:
        coords = (i.x * 32 - LowX.x * 32, i.y * 32 - LowY.y * 32)
        StaticSurface.blit(i.Wallsurface, coords, special_flags=pygame.BLEND_ALPHA_SDL2)
        StaticSurface.blit(i.Floorsurface, coords, special_flags=pygame.BLEND_ALPHA_SDL2)

        progress.add()
        progress.update()
        pygame.display.update()

    progress = ProgressBar(FinalStaticSurface.get_width()/4, "Exporting Lighting")
    progress.update()
    pygame.display.update()

    for x in range(FinalStaticSurface.get_width()):
        for y in range(FinalStaticSurface.get_height()): 

            color = StaticSurface.get_at((x,y))

            if color != (0,0,0,0):

                alpha = Clamp(LightSurface.get_at((x,y))[3], LightManager.GlobalLightLevel, 255) / 210

                r = Clamp(color[0] * alpha, 0,255)
                g = Clamp(color[1] * alpha, 0,255)
                b = Clamp(color[2] * alpha, 0,255)

                color = (r,g,b)

                pygame.draw.rect(FinalStaticSurface, color, pygame.Rect(x, y, 1, 1))

        if x % 4 == 1:
            progress.add()
            progress.update()
            pygame.display.update()

    os.chdir(dir)

    os.mkdir(dir + "Export")


        
    pygame.image.save(FinalStaticSurface, f"{dir}Export\\LevelSurface.png")

    with open(f"{dir}Export\\LevelSurfaceOffset.txt", "w") as file:
        file.write(f"{LowX.x}, {LowY.y}")

    zipped = shutil.make_archive(LevelName, "zip", dir + "Export")

    shutil.rmtree(dir + "Export")

    print("Level Exported!")