SelectedTool = 0

def returnSelectedTool():
    return SelectedTool

def ChangeSelectedTool(tool): # function to manage which tool is selected - tools are the different "brushes" used to create the maps
    global SelectedTool
    if tool == "Wall":
        SelectedTool = 1
    elif tool == "Floor":
        SelectedTool = 2
    elif tool == "Light":
        SelectedTool = 4

    else:
        SelectedTool = 0
        
        
SelectedWallTexture = False