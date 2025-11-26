import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.w = 28
        self.h = 36

        self.health = 120
        self.speed = 4

        self.facing = (1, 0)

        self.attack_timer = 0
        self.invuln = 0

        self.base_damage = 20
        # inventory: can store by level (int) or by name (str)
        self.inventory = {}
        self.current_weapon_level = None
        self.current_weapon = None
        self.equipped = False

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.w/2),
            int(self.y - self.h/2),
            self.w, self.h
        )

    def add_weapon(self, weapon, level=None):
        """Agrega un arma al inventario. Si level es int, la guarda con esa clave, si no usa el nombre."""
        copy = weapon.copy()
        if level is not None:
            self.inventory[level] = copy
        else:
            self.inventory[copy["name"]] = copy

    def equip_by_level(self, level):
        if level in self.inventory:
            self.current_weapon_level = level
            self.current_weapon = self.inventory[level]
            self.equipped = True

    def equip_best_melee(self):
        """Equipar la mejor arma cuerpo a cuerpo disponible (mayor daño)."""
        best = None
        best_key = None
        for k, w in self.inventory.items():
            if not w.get("ranged", False):
                if best is None or w.get("damage", 0) > best.get("damage", 0):
                    best = w
                    best_key = k
        if best:
            self.current_weapon = best
            # if key is an int, set current_weapon_level
            if isinstance(best_key, int):
                self.current_weapon_level = best_key
            self.equipped = True
        else:
            # sin arma cuerpo a cuerpo -> desequipar
            self.current_weapon = None
            self.current_weapon_level = None
            self.equipped = False

    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            mag = math.hypot(dx, dy)
            if mag != 0:
                dx /= mag
                dy /= mag

            self.x += dx * self.speed
            self.y += dy * self.speed

            self.x = max(self.w/2, min(self.x, SCREEN_WIDTH - self.w/2))
            self.y = max(self.h/2, min(self.y, SCREEN_HEIGHT - self.h/2))

            self.facing = (dx, dy)

    def start_attack(self):
        if self.equipped and self.attack_timer <= 0:
            self.attack_timer = 12

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.invuln > 0:
            self.invuln -= 1

    def draw(self, surf):
        pygame.draw.rect(surf, (50,150,230), self.rect)

        # Cara / dirección
        fx = self.x + self.facing[0] * self.w/2
        fy = self.y + self.facing[1] * self.h/2
        pygame.draw.circle(surf, (255,255,255), (int(fx), int(fy)), 4)

        # Indicador de arma equipada
        if self.equipped and self.current_weapon:
            wx = self.x + self.facing[0] * (self.w/2 + 6)
            wy = self.y + self.facing[1] * (self.h/2 + 6)
            color = (220,220,50) if not self.current_weapon.get("ranged") else (120,80,40)
            pygame.draw.rect(surf, color, (wx-4, wy-4, 8, 8))

    def get_attack_hitbox(self):
        if self.attack_timer <= 0:
            return None

        fx, fy = self.facing
        if fx == 0 and fy == 0:
            fx, fy = (1, 0)

        cx = self.x + fx * (self.w/2 + 20)
        cy = self.y + fy * (self.h/2 + 20)

        return pygame.Rect(int(cx - 20), int(cy - 20), 40, 40)

    def effective_damage(self):
        if self.current_weapon:
            return self.current_weapon.get("damage", self.base_damage)
        return self.base_damage
