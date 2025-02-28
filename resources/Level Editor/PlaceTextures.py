import pygame


class SelectionArea():
    def __init__(self, color, surface):
        
        self.color = color
        self.surface = surface
        
    def update(self, coords, scale):
        x, y = coords
        w, h = scale
        pygame.draw.rect(self.surface, self.color, pygame.Rect(x, y, w, h), 3)