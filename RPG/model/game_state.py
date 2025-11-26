from .player import Player
from .enemy import Enemy, Boss
from .projectile import Arrow
from .pickup import Pickup
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Armas por nivel (index 1 -> nivel 1)
LEVEL_WEAPONS = [
    {"name": "Hacha oxidada", "damage": 35, "ranged": False},
    {"name": "Espada corta", "damage": 50, "ranged": False},
    {"name": "Lanza",        "damage": 70, "ranged": False},
    {"name": "Espada larga", "damage": 95, "ranged": False},
    {"name": "Arco",         "damage": 120, "ranged": True},
]

# Arma inicial del jugador
STARTING_WEAPON = {"name": "Daga inicial", "damage": 18, "ranged": False}

class GameState:
    def __init__(self):
        self.FPS = 60

        # Crear jugador con arma inicial equipada
        self.player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.player.add_weapon(STARTING_WEAPON, level=0)
        self.player.current_weapon = STARTING_WEAPON.copy()
        self.player.equipped = True

        # Un arma adicional cerca del centro (drop visible)
        ax = SCREEN_WIDTH/2 + 80
        ay = SCREEN_HEIGHT/2 - 60
        # spawn a level-1 pickup as demonstration (player can pick it up)
        self.pickups = [Pickup(ax, ay, 1)]

        self.arrows = []
        self.current_enemy = None

        self.defeated = 0
        self.level = 0
        self.obtained_weapon_levels = set()

        # Flags for boss sequence
        self.spawn_bow_before_boss = False
        self.spawn_boss_next = False
        self.upcoming_level_for_drop = None

    def spawn_enemy(self, level, force_boss=False, drop_weapon_level=None):
        return Enemy.spawn(level, force_boss, drop_weapon_level)

    def spawn_arrow(self):
        p = self.player
        fx, fy = p.facing
        if fx == 0 and fy == 0:
            fx, fy = (1, 0)

        arrow = Arrow(
            p.x + fx * (p.w/2 + 8),
            p.y + fy * (p.h/2 + 8),
            fx * 10,
            fy * 10,
            p.effective_damage()
        )
        self.arrows.append(arrow)

    def update(self):
        # clamp player health to min 0
        if self.player.health < 0:
            self.player.health = 0

        # Actualizar jugador
        self.player.update()

        # Actualizar flechas
        for a in self.arrows:
            a.update()
        self.arrows = [a for a in self.arrows if a.alive]

        # SPAWN DE ENEMIGOS
        if (self.current_enemy is None or not self.current_enemy.alive):
            # Si murió el anterior, contabilizar
            if self.current_enemy is not None and not self.current_enemy.alive:
                was_boss = isinstance(self.current_enemy, Boss)
                # drop weapon if had
                if self.current_enemy.will_drop_weapon_level:
                    lvl = self.current_enemy.will_drop_weapon_level
                    self.pickups.append(Pickup(self.current_enemy.x, self.current_enemy.y, lvl))
                # contar como derrotado
                self.defeated += 1

                # Si el que murió era jefe, revertir a mejor arma melee disponible
                if was_boss:
                    self.player.equip_best_melee()

                self.current_enemy = None

            # calcular nivel actual en base a derrotas (5 kills => level 1)
            new_level = self.defeated // 5
            if new_level > self.level:
                # Subimos de nivel
                self.level = new_level
                # Si el nuevo nivel es múltiplo de 5 planeamos bow->boss
                if self.level % 5 == 0 and self.level > 0:
                    # marcar que queremos que el próximo enemigo normal dropee el arma para este nivel
                    self.spawn_bow_before_boss = True
                    self.upcoming_level_for_drop = self.level

            # Si toca spawnear jefe ahora
            if self.spawn_boss_next:
                self.current_enemy = self.spawn_enemy(self.level, force_boss=True)
                self.spawn_boss_next = False
            else:
                drop = None
                if self.spawn_bow_before_boss and self.upcoming_level_for_drop is not None:
                    # hacemos que este enemigo dropee arma para el próximo boss level
                    drop = self.upcoming_level_for_drop
                    self.spawn_bow_before_boss = False
                    # cuando muera ese enemigo, spawn_boss_next se activará para spawnear el jefe
                    self.spawn_boss_next = True
                    # mantenemos upcoming_level_for_drop para referencia
                else:
                    # spawn de rutina; si no tienes arma de este nivel, se puede forzar drop (opcional)
                    if 1 <= self.level <= len(LEVEL_WEAPONS):
                        if self.level not in self.obtained_weapon_levels:
                            # Forzamos que el primer enemigo después del nivel suba dropee el arma
                            drop = self.level
                self.current_enemy = self.spawn_enemy(self.level, force_boss=False, drop_weapon_level=drop)

        # INTERACCIONES con enemigo actual
        if self.current_enemy and self.current_enemy.alive:
            e = self.current_enemy
            e.update(self.player)

            # Golpe al jugador
            if e.rect.colliderect(self.player.rect):
                if self.player.invuln <= 0:
                    dmg = max(4, 8 + e.level//2)
                    self.player.health -= dmg
                    # clamp
                    if self.player.health < 0:
                        self.player.health = 0
                    self.player.invuln = 30

            # Golpe del jugador (melee)
            hitbox = self.player.get_attack_hitbox()
            if hitbox and e.rect.colliderect(hitbox):
                e.take_damage(self.player.effective_damage())

            # Flechas impactan
            for a in self.arrows:
                # use integer coordinates for collide check
                if e.rect.collidepoint(int(a.x), int(a.y)):
                    e.take_damage(a.damage)
                    a.alive = False

        # PICKUPS
        for p in self.pickups[:]:
            if self.player.rect.colliderect(p.rect):
                wlvl = p.weapon_level
                if wlvl not in self.obtained_weapon_levels:
                    self.obtained_weapon_levels.add(wlvl)
                    weapon = LEVEL_WEAPONS[wlvl-1].copy()
                    # add to inventory keyed by level
                    self.player.add_weapon(weapon, level=wlvl)
                    # equip the weapon automatically (player should have the bow before boss)
                    self.player.current_weapon = weapon.copy()
                    self.player.current_weapon_level = wlvl
                    self.player.equipped = True
                self.pickups.remove(p)
