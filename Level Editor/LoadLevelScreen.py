import FetchSavedLevels as FSL
import pygame, CreateNewLevel

LevelToLoad = ""

def Run():
    Window = pygame.display.set_mode((300,500))
    pygame.display.set_caption("Select Level")

    SavedLevels = FSL.Fetch() # Fetches all levels in "Levels" Directory and saves them as a list

    font = pygame.font.SysFont("ariel", 50)

    class Levels(pygame.sprite.Sprite): # class to render all levels picked up in "Levels" directory
        def __init__(self, y, name, new):
            super().__init__()
            self.y = y
            self.name = name
            self.new = new

        def update(self):

            rect = pygame.Rect(0, self.y, 300, 50) # rect used for collision detection between mouse and level obj

            if pygame.Rect.collidepoint(rect, pygame.mouse.get_pos()):
                if (pygame.mouse.get_pressed()[0]): # if clicked on this obj, send the level name to LevelToLoad Variable
                    global LevelToLoad
                    if self.new:
                        CreateNewLevel.Create(createLevel)
                        return
                    LevelToLoad = self.name
                pygame.draw.rect(Window, "grey", rect)

            if self.new:
                text = font.render(self.name, True, "green")
            else:
                text = font.render(self.name, True, "white")

            text_rect = text.get_rect(center=(150, self.y+25))

            Window.blit(text, text_rect)

    LevelsGroup = pygame.sprite.Group()

    for i in range(len(SavedLevels)):  # loops through all levels in "Levels" directory and creates a Levels object of them
            LevelsGroup.add(Levels(i*50, SavedLevels[i-1], False))
    LevelsGroup.add(Levels(len(SavedLevels)*50, "New Level", True))

    while True:
        
        if LevelToLoad != "": # if this variable changes - return to level editor to select that level to load into editor
            pygame.quit()
            return LevelToLoad

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        Window.fill("black")

        LevelsGroup.update()

        pygame.display.update()
        
def createLevel(name):
    global LevelToLoad
    LevelToLoad = name