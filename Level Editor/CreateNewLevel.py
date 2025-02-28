import tkinter, os

def GenerateFiles(name, func):
    if name == "":
        return
    
    GlobalFilePath = __file__.removesuffix("\\Level Editor\\CreateNewLevel.py")+"\\Levels"
    folder = GlobalFilePath + "\\" + name
    
    os.mkdir(folder)
    os.chdir(folder)
    
    os.mkdir("Chunks")
    
    with open("Level.lvl", "w") as f:
        f.write("0,0")
        
    func(name)
    global window
    window.destroy()

def Create(func):

    global window
    window = tkinter.Tk()
    window.geometry("250x300")
    window.resizable(0,0)
    window.title("Create Level")

    LevelName = tkinter.StringVar()
    LevelNameText = tkinter.Label(text="Level Name:")
    LevelNameText.pack(pady=10)
    LevelNameEntry = tkinter.Entry(textvariable=LevelName)
    LevelNameEntry.pack()


    CreateLevelButton = tkinter.Button(text="Create", command= lambda: GenerateFiles(LevelName.get(), func), fg = "green")
    CreateLevelButton.pack(pady=10)


    window.mainloop()