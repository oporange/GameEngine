from Imports import *
import pygame, math
import Fonts, GlobalInputManager

def Clamp(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    else:
        return val
    
# All Code for the Tool/Menu bar
class MenuBar(): # Main class for the toolbar GUI element
    
    def __init__(self, y):
        
        self.y = y
        
        self.Menus = []
        
        self.widths = []

    def Add(self, text):
        self.Menus.append( MenuBarChild(text, self, self.widths) )
        
    def AddChild(self, parent, name, func, alias):
        for i in self.Menus:
            if i.text == parent:
                i.AddChild(name, func, alias)
        
    def update(self):
        pygame.draw.rect(pygame.display.get_surface(), "blue", pygame.Rect(0, self.y, pygame.display.get_window_size()[0], 20))
        
        for i in range(len(self.Menus)):
            width = 0
            for j in range(i):
                width += self.widths[j]
            self.Menus[i].update(width, self.y)
        
        
class MenuBarChild(): # first child node of the toolbar GUI element
    
    def __init__(self, name, parent, widths):
        
        self.text = name
        
        self.active = False

        self.parent = parent
        
        pygame.init()
        
        self.font = Fonts.KongText9

        self.ChildNodes = []
        self.LongestText = 0

        self.CollideMouseRect = pygame.Rect(0,0,1,1)

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.ClickFunc)


        self.width = self.font.render(self.text, "white")[1].w + 10
        widths.append(self.width)
        
    def AddChild(self, name,func, alias):
        rects=[]
        self.ChildNodes.append(MenuBarChildChild(name, func, alias))
        for i in self.ChildNodes:
            rects.append(i.GetRect())
        rects=sorted(rects,key = lambda rect: rect[2])
        self.LongestText = rects[-1][2] + 6
    

    def update(self, x, y):
        self.CollideMouseRect = pygame.Rect(x,y,self.width,20)
        collide = self.CollideMouseRect.collidepoint(pygame.mouse.get_pos())
        
        if collide:
            pygame.draw.rect(pygame.display.get_surface(), "cyan", self.CollideMouseRect)
        else:
            pygame.draw.rect(pygame.display.get_surface(), "blue", self.CollideMouseRect)
            
            
        for i in range(len(self.ChildNodes)):
            self.ChildNodes[i].active = self.active
            self.ChildNodes[i].update(x, y + 15*i + 20, self.LongestText)


        pygame.display.get_surface().blit(self.font.render(self.text, "white")[0], (x+2, y+5))
        pygame.draw.rect(pygame.display.get_surface(), "grey", pygame.Rect(x+self.width-2, y, 1, 20))

    def ClickFunc(self):
        if not self.CollideMouseRect.collidepoint(pygame.mouse.get_pos()):
            self.active = False
        else:
            self.active = not self.active
            if self.active:
                for i in self.parent.Menus:
                    if i != self:
                        i.active = False
            return True
        
class MenuBarChildChild(): # second level node for the toolbar GUI element
    
    def __init__(self, text, func, alias):
        
        self.text = text
        self.func = func
        
        self.font = Fonts.KongText8

        self.active = False
        
        self.rect = self.font.render(self.text, "white")[1]
        
        if alias:
            GlobalInputManager.AddAlias(alias, self.func)

        self.CollideMouseRect = pygame.Rect(0, 0, 10, 15)

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.ClickFunc)
        
    def GetRect(self):
        return self.rect
        
    def update(self, x, y, width):
        
        if self.active:
            self.CollideMouseRect = pygame.Rect(x, y, width, 15)
            
            collide = self.CollideMouseRect.collidepoint(pygame.mouse.get_pos())
            
            if collide:
                pygame.draw.rect(pygame.display.get_surface(), "light blue 4", self.CollideMouseRect)
            else:
                pygame.draw.rect(pygame.display.get_surface(), "light blue", self.CollideMouseRect)
            
            pygame.display.get_surface().blit(self.font.render(self.text, "white")[0], (x+2, y+5))

    def ClickFunc(self):
        if self.CollideMouseRect.collidepoint(pygame.mouse.get_pos()) and self.active:
            self.func()
            self.active = False
            return True

#-----------------------------------------------------------------------------------------------------

#Class to display a grid on the screen
class Grid():
    def __init__(self, size, screenSize):
        self.size = size
        self.screenSize = screenSize
        self.surface = pygame.Surface((screenSize[0] + self.size*2, screenSize[1] + self.size*2))
        
        for x in range(math.ceil(self.screenSize[0]/self.size + self.size*2)):
            for y in range(math.ceil(self.screenSize[1]/self.size + self.size*2)):
                pygame.draw.rect(self.surface, "white", pygame.Rect(x*self.size - self.size, y*self.size - self.size, self.size, self.size), 1)
                
        self.display = False
    
    def Show(self):
        self.display = not self.display

    def Size(self, size):
        self.size *= size
        
        self.surface = pygame.Surface((self.screenSize[0] + self.size*2, self.screenSize[1] + self.size*2))
        self.surface.fill("black")
        
        for x in range(math.ceil(self.screenSize[0]/self.size + self.size*2)):
            for y in range(math.ceil(self.screenSize[1]/self.size + self.size*2)):
                pygame.draw.rect(self.surface, "white", pygame.Rect(x*self.size, y*self.size, self.size, self.size), 1)
                
    def update(self, Offset):
        if self.display:
            pygame.display.get_surface().blit(self.surface,(0 + Offset[0] - self.size,0 + Offset[1] - self.size))
            
#----------------------------------------------------------------------------------------------------------------------------

# classes for different kinds of clickable buttons           
class Button():
    def __init__(self, x, y, texture, ClickFunc): #  function to handle buttons on UI
        
        self.x = x
        self.y = y
        
        self.texture = texture.copy()

        self.BrightTexture = pygame.Surface(texture.get_size())
        self.BrightTexture = texture.copy()
        self.BrightTexture.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)

        self.rect = texture.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.ClickFunc = ClickFunc

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.ClickCheck)
    
    def update(self):
        MousePos = pygame.mouse.get_pos()

        if pygame.Rect.collidepoint(self.rect, MousePos):
            pygame.display.get_surface().blit(self.BrightTexture, (self.x, self.y))
        else:
            pygame.display.get_surface().blit(self.texture, (self.x, self.y))

    def ClickCheck(self):
        MousePos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.rect, MousePos):
            self.ClickFunc()
            return True

class Switch():
    def __init__(self, x, y, texture, SwitchGroup, *ClickFunc): #  function to handle toggleable buttons on UI
        
        self.x = x
        self.y = y
        
        self.SwitchGroup = SwitchGroup
        if SwitchGroup:
            SwitchGroup.AddSwitch(self)

        self.texture = texture.copy()

        self.HoverTexture = texture.copy()
        self.HoverTexture.fill((30, 30, 30), special_flags=pygame.BLEND_RGB_ADD)

        self.ToggledTexture = texture.copy()
        self.ToggledTexture.fill((80, 80, 80), special_flags=pygame.BLEND_RGB_ADD)

        self.rect = texture.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.Toggled = False
        self.ClickFunc = ClickFunc[0]
        self.DeselectFunc = ClickFunc[1]

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.ClickCheck)
    
    def update(self):
        MousePos = pygame.mouse.get_pos()

        if self.Toggled:
            pygame.display.get_surface().blit(self.ToggledTexture, (self.x, self.y))
        elif pygame.Rect.collidepoint(self.rect, MousePos):
            pygame.display.get_surface().blit(self.HoverTexture, (self.x, self.y))
        else:
            pygame.display.get_surface().blit(self.texture, (self.x, self.y))

    def ClickCheck(self):
        MousePos = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(self.rect, MousePos):
            if not self.Toggled:
                if self.SwitchGroup:
                    self.SwitchGroup.SwitchPressed(self)

                self.ClickFunc()
            if self.Toggled:
                self.DeselectFunc()
            self.Toggled = not self.Toggled
            return True

class ExclusiveSwitchManager():  # class to manage groups of switches that should be exlcusive (only 1 active at a time)
    def __init__(self):
        self.switches = []

    def AddSwitch(self, switch):
        self.switches.append(switch)

    def SwitchPressed(self, switch):
        for i in self.switches:
            if i != switch:
                i.Toggled = False
#----------------------------------------------------------------------------------------------------

class DropdownUI():
    def __init__(self, x, y, title, ItemsToList, ActiveVar, whenEquals, SelectedVar): # Active var is the variable used to determine if the dropdown should be shown
        self.x = x                                                # whenEquals is the state of ActiveVar when the dropdown is active     
        self.y = y

        self.title = title

        self.ItemsToList = []

        self.ActiveVar = ActiveVar
        self.WhenEquals = whenEquals

        self.selected = 0
        self.VarToSetSelected = SelectedVar

        rows = math.floor(len(ItemsToList) / 4)
        listIndexCount = 0
        for i in range(rows):
            l = i*4
            self.ItemsToList.append([ItemsToList[l], ItemsToList[l+1], ItemsToList[l+2], ItemsToList[l+3]])
            listIndexCount += 4

        ItemsLeft = len(ItemsToList) - listIndexCount
        lastrow = []
        for i in range(ItemsLeft):
            lastrow.append(ItemsToList[0-(ItemsLeft-i)])
        self.ItemsToList.append(lastrow)
        
        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.ClickFunc)
        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickReleaseCmds, 0, self.ClickUpFunc)

        self.drag = False

    def update(self):
        if self.ActiveVar() == self.WhenEquals:
            self.rect = pygame.draw.rect(pygame.display.get_surface(), "blue", pygame.Rect(self.x, self.y, 178, 198))
            barRect = pygame.draw.rect(pygame.display.get_surface(), "light blue 4", pygame.Rect(self.x, self.y, 178, 20))
            closeRect = pygame.draw.rect(pygame.display.get_surface(), "red", pygame.Rect(self.x+158, self.y, 20, 20))
            
            if (pygame.Rect.collidepoint(closeRect, pygame.mouse.get_pos())):
                if pygame.mouse.get_pressed()[0]:
                    #close menu
                    pass
                
                pygame.draw.rect(pygame.display.get_surface(), "indianred", pygame.Rect(self.x+158, self.y, 20, 20))
            elif self.drag:
                self.x, self.y = pygame.mouse.get_pos()
                self.x -= 178/2
                self.y -= 10
                self.x = Clamp(self.x, 0, 1280 - self.rect.w)
                self.y = Clamp(self.y, 0, 736 - self.rect.h)

            text = Fonts.KongText9.render(self.title, "white")[0]
            Trect = Fonts.KongText9.render(self.title, "white")[1]

            pygame.display.get_surface().blit(text, (self.x+2, self.y + 10 - Trect.y/2))
            
            index = 0
            for i in range(len(self.ItemsToList)):
                lis = self.ItemsToList[i]
                for j in range(len(lis)):
                    x = self.x + 10 + 42*j
                    y = self.y + 30 + 42*i
                    
                    rect = pygame.Rect(x-2, y-2, 36, 36)
                    
                    if (pygame.Rect.collidepoint(rect, pygame.mouse.get_pos()) or self.selected == index):
                        pygame.draw.rect(pygame.display.get_surface(), "grey", rect)
                    else:
                        pygame.draw.rect(pygame.display.get_surface(), "black", rect)
                        
                    pygame.display.get_surface().blit(lis[j].ReturnImg(), (x, y))

                    index += 1

            self.Selected()

    def Selected(self):

        index = math.floor((self.selected)/4)
        index = self.ItemsToList[index][(self.selected)%4]

        return index
    
    def ClickFunc(self):
            if self.ActiveVar() == self.WhenEquals:
                index = 0
                for i in range(len(self.ItemsToList)):
                    lis = self.ItemsToList[i]
                    for j in range(len(lis)):
                        x = self.x + 10 + 42*j
                        y = self.y + 30 + 42*i
                        
                        rect = pygame.Rect(x-2, y-2, 36, 36)
                        
                        if (pygame.Rect.collidepoint(rect, pygame.mouse.get_pos()) and (pygame.mouse.get_pressed()[0])):
                            self.selected = index
                            self.VarToSetSelected = self.Selected().reference
                            return True
                        index += 1
                if pygame.Rect.collidepoint(pygame.Rect(self.x, self.y, 178, 20), pygame.mouse.get_pos()):
                    self.drag = True
                    return True
                if pygame.Rect.collidepoint(pygame.Rect(self.x, self.y, 178, 198), pygame.mouse.get_pos()):
                    return True
            
    def ClickUpFunc(self):
        self.drag = False
                
            
class GuiItem():  # Class for items being rendered and accessed in dropdowns
    def __init__(self, img, reference):
        
        self.img = img
        self.reference = reference
        
    def ReturnImg(self):
        return self.img
    
#------------------------------------------------------------------------------------------------------------

class ProgressBar():    #  class to display progress bars to the screen
    def __init__(self, ItemCount, title):   # item count is the number of items for the progress bar to keep track of - currentItem / ItemCount = percentage
        
        self.width = 440
        self.height = 140

        self.ItemCount = ItemCount
        self.currentItem = 0

        self.title = title

        self.rect = pygame.Rect((1280 - self.width)/2, (736 - self.height)/2, self.width, self.height)

    def update(self):

        pygame.draw.rect(pygame.display.get_surface(), "blue", self.rect)
        pygame.draw.rect(pygame.display.get_surface(), "light blue 4", pygame.Rect((1280 - self.width)/2, (736 - self.height)/2, self.width, 20))

        text = Fonts.KongText11.render(self.title, "white")[0]
        Trect = Fonts.KongText11.render(self.title, "white")[1]
        pygame.display.get_surface().blit(text, ((1280 - self.width)/2 + 2, (736 - self.height)/2 + 10 - Trect.y/2))

        comepletion = self.currentItem / self.ItemCount

        pygame.draw.rect(pygame.display.get_surface(), "dodgerblue3", pygame.Rect(self.rect.x + 10, self.rect.y + self.height/2, self.width - 20, 40))
        pygame.draw.rect(pygame.display.get_surface(), "deepskyblue", pygame.Rect(self.rect.x + 10, self.rect.y + self.height/2, (self.width - 20) * comepletion, 40))

    def add(self):

        self.currentItem += 1

#----------------------------------------------------------------------------------------------------------------------------------------

class ParameterEditor():
    def __init__(self, x, y, title):
        
        self.title = title

        self.x = x
        self.y = y

        self.width = 400
        self.height = 50

        self.Parameters = []
        self.ParameterHeights = []

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey("black")

    def update(self):

        pygame.draw.rect(pygame.display.get_surface(), "blue", pygame.Rect(self.x, self.y, self.width, self.height))

        self.surface.fill("black")

        HeightTracker = 0

        for i in range(len(self.Parameters)):
            self.Parameters[i].update(10 + HeightTracker, self.x, self.y)
            HeightTracker += self.ParameterHeights[i]

        pygame.display.get_surface().blit(self.surface, (self.x, self.y))


    def AddParameter(self, parameter, ChangeFunc, startNum):
        
        newParam = parameter(self.surface, ChangeFunc, startNum)
        self.ParameterHeights.append(newParam.height)
        self.Parameters.append(newParam)

class Slider():
    def __init__(self, surf, ChangeFunc, startPercent):

        self.surf = surf
        self.height = 10

        self.PercentFilled = startPercent
        self.SlidePos = 350 * self.PercentFilled

        self.ChangeFunc = ChangeFunc

        self.grabbed = False

        self.sliderRect = pygame.Rect(0,0,0,0)

        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickCmds, 0, self.LeftClickFunc)
        GlobalInputManager.AddCMD(GlobalInputManager.LeftClickReleaseCmds, 0, self.LeftUnclickFunc)

    def update(self, y, Gx, Gy):

        pygame.draw.rect(self.surf, "grey", pygame.Rect(25, y, 350, self.height))

        self.sliderRect = pygame.Rect(Gx + self.SlidePos + 25, Gy + y - 5, 20, self.height + 10)

        if self.grabbed:
            self.SlidePos = Clamp(pygame.mouse.get_pos()[0] - (Gx + 25) - 10, 0, 350)
            self.PercentFilled = self.SlidePos / 350

            self.ChangeFunc(self.PercentFilled)

        if pygame.Rect.collidepoint(self.sliderRect, pygame.mouse.get_pos()) or self.grabbed:
            pygame.draw.rect(self.surf, "lavender ", pygame.Rect(25 + self.SlidePos, y - 5, 20, self.height + 10))
        else:
            pygame.draw.rect(self.surf, "light grey", pygame.Rect(25 + self.SlidePos, y - 5, 20, self.height + 10))

    def LeftClickFunc(self):
        if pygame.Rect.collidepoint(self.sliderRect, pygame.mouse.get_pos()):
            self.grabbed = True
            return True

    def LeftUnclickFunc(self):
        self.grabbed = False


class MouseManager():
    def __init__(self):

        self.type = 0

    def ChangeCursor(self, typ):

        if typ == self.type:
            return False
        
        self.type = typ
        
        if typ == 0:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif typ == 1:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        elif typ == 2:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        elif typ == 3:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        elif typ == 4:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAITARROW)
        elif typ == 5:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
        elif typ == 6:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)    

Cursor = MouseManager()



print("GUI Loaded!")