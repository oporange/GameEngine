import os

def Fetch():
    LevelsDirectory = __file__.removesuffix("\\Level Editor\\FetchSavedLevels.py")+"\\Levels"

    return os.listdir(LevelsDirectory)

