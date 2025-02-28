import pygame, math, os



class Entity():
    def __init__(self, x, y, texture, collisionRect, ShadowRect): # posX, posY, Draw texture, rect used for collision, surface used to render realtime shadows (False if disabled)
        
        self.x = x
        self.y = y
        self.texture = texture
        self.rect = collisionRect
        self.ShadowRect = ShadowRect
        
        
    def update(self):
        
        pygame.display.get_surface().blit(self.texture, (self.x, self.y))
        
        
class EntityGroup():
    def __init__(self):
        
        self.list = []
        
    def add(self, ent):
        
        self.list.append(ent)