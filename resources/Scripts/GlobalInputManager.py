from Imports import *
import pygame

class PriorityLevels():
    def __init__(self):
        
        self.List = []
        
    def AddCMD(self, index, cmd):
        self.List.insert(index, cmd)
        
    def ReturnLevel(self):
        return self.List
        

Aliases = [] # aliases are commands bound to different functions - usually for commands in the toolbar menu
LeftClickCmds = PriorityLevels() # any command that requires a left click (once) from the mouse, uses levels of priority to determine where mouse input should be used
LeftClickReleaseCmds = PriorityLevels() #  any command that requires the left click to be released
RightClickCmds = PriorityLevels() # any command that requires a right click (once) from the mouse
RightClickReleaseCmds = PriorityLevels()#  any command that requires the right click to be released
MiddleClickCmds = PriorityLevels() # any command that requires a middle click (once) from the mouse
MiddleClickReleaseCmds = PriorityLevels()#  any command that requires the middle click to be released

LclickFrame = False
RclickFrame = False
MclickFrame = False

def GlobalInput(event):
    global LclickFrame, RclickFrame, MclickFrame

    if event.type == pygame.QUIT:
        quit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            quit()
        for i in Aliases:
            if event.key == i[0]:
                i[1]()

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            LclickFrame = True
            for i in LeftClickCmds.ReturnLevel(): # loops through all functions in the list to call their left click cmd
                    if i():
                        break
        elif event.button == 3:
            RclickFrame = True
            for i in RightClickCmds.ReturnLevel():
                if i():
                    break
        elif event.button == 2:
            MclickFrame = True
            for i in MiddleClickCmds.ReturnLevel():
                if i():
                    break

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            for i in LeftClickReleaseCmds.ReturnLevel():
                if i():
                    break
        elif event.button == 3:
            for i in RightClickReleaseCmds.ReturnLevel():
                if i():
                    break
        elif event.button == 2:
            for i in MiddleClickReleaseCmds.ReturnLevel():
                if i():
                    break
    else:
        return 0
    
def update():
    global LclickFrame, RclickFrame, MclickFrame
    LclickFrame = False
    RclickFrame = False
    MclickFrame = False
    
def AddAlias(key, cmd):
    Aliases.append((key, cmd))
    
def AddCMD(cmdList, priority, cmd):
    cmdList.AddCMD(priority, cmd)
    

    
print("Input Loaded!")
    