import random
import math
import pygame

ENEMY_BASE_HP = 300
ENEMY_HP_PER_LEVEL = 5
ENEMY_BASE_SPEED = 1.5
ENEMY_SPEED_PER_LEVEL = 0.05
BOSS_HP_MULTIPLIER = 20

def random_spawn_point():
    side = random.choice(["left", "right", "top", "bottom"])
    if side == "left": return -40, random.uniform(0, 600)
    if side == "right": return 840, random.uniform(0, 600)
    if side == "top": return random.uniform(0,800), -40
    return random.uniform(0,800), 640


class Enemy:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = level

        self.r = 16
        self.color = (200,50,50)

        self.max_hp = ENEMY_BASE_HP + level * ENEMY_HP_PER_LEVEL
        self.hp = self.max_hp

        self.speed = ENEMY_BASE_SPEED + level * ENEMY_SPEED_PER_LEVEL
        self.alive = True

        self.will_drop_weapon_level = None

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r*2, self.r*2)

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        d = max(1, math.hypot(dx,dy))

        self.x += (dx/d) * self.speed
        self.y += (dy/d) * self.speed

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.r)
        hp_w = int((self.hp/self.max_hp) * (self.r*2))
        pygame.draw.rect(surf, (40,40,40), (int(self.x-self.r), int(self.y-self.r-10), self.r*2, 6))
        pygame.draw.rect(surf, (50,200,50), (int(self.x-self.r), int(self.y-self.r-10), hp_w, 6))

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    @classmethod
    def spawn(cls, level, force_boss=False, drop_weapon_level=None):
        if force_boss:
            x,y = random_spawn_point()
            e = Boss(x,y,level)
        else:
            x,y = random_spawn_point()
            e = cls(x,y,level)

        if drop_weapon_level:
            e.will_drop_weapon_level = drop_weapon_level

        return e


class Boss(Enemy):
    def __init__(self, x, y, level):
        super().__init__(x, y, level)
        self.r = 28
        self.color = (160,40,200)
        self.max_hp = (ENEMY_BASE_HP + level * ENEMY_HP_PER_LEVEL) * BOSS_HP_MULTIPLIER
        self.hp = self.max_hp
        self.speed = max(0.8, ENEMY_BASE_SPEED + level * ENEMY_SPEED_PER_LEVEL * 0.5)
