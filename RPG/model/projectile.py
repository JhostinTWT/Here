import pygame

class Arrow:
    def __init__(self, x, y, vx, vy, damage):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.r = 4
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Fuera de pantalla
        if not (0 <= self.x <= 800 and 0 <= self.y <= 600):
            self.alive = False

    def draw(self, surf):
        pygame.draw.circle(surf, (120,80,40), (int(self.x), int(self.y)), self.r)
