import pygame

class Pickup:
    def __init__(self, x, y, weapon_level):
        self.x = x
        self.y = y
        self.weapon_level = weapon_level
        self.w = 18
        self.h = 18

    @property
    def rect(self):
        return pygame.Rect(int(self.x-self.w/2), int(self.y-self.h/2), self.w, self.h)

    def draw(self, surf):
        pygame.draw.rect(surf, (230,230,50), self.rect)

