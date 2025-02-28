from Imports import *

class screen():
    def __init__(self):

        self.ScrW = 1280
        self.ScrH = 736

        self.Title = "Window"

        self.window = pygame.display.set_mode((self.ScrW, self.ScrH))
        pygame.display.set_caption(self.Title)

    def SetTitle(self, title):
        self.Title = title
        pygame.display.set_caption(title)
        
    def fill(self, color):
        self.window.fill(color)

print("Window Loaded!")