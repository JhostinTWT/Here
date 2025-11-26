import pygame

class Renderer:
    def __init__(self, window, state):
        self.win = window
        self.state = state
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 40)

    def render(self):
        self.win.fill((30,30,30))

        # Pickups
        for p in self.state.pickups:
            p.draw(self.win)

        # Enemy
        if self.state.current_enemy and self.state.current_enemy.alive:
            self.state.current_enemy.draw(self.win)

        # Player
        self.state.player.draw(self.win)

        # Arrows
        for a in self.state.arrows:
            a.draw(self.win)

        self.draw_hud()
        pygame.display.flip()

    def draw_hud(self):
        p = self.state.player

        # Vida
        pygame.draw.rect(self.win, (40,40,40), (10,10,200,20))
        # clamp hp display denominator safely (use 120 as max)
        hp_w = int((max(0, p.health) / 120) * 200)
        pygame.draw.rect(self.win, (50,200,50), (10,10,hp_w,20))
        self.win.blit(self.font.render(f"HP: {int(p.health)}", True, (255,255,255)), (15,12))

        # Stats
        self.win.blit(self.font.render(f"Kills: {self.state.defeated}", True, (255,255,255)), (10,40))
        self.win.blit(self.font.render(f"Nivel: {self.state.level}", True, (255,255,255)), (10,65))

        # Arma equipada
        if p.current_weapon:
            w = p.current_weapon
            txt = f"Arma: {w['name']}  DMG:{w['damage']}"
            self.win.blit(self.font.render(txt, True, (255,255,255)), (10,90))
        else:
            self.win.blit(self.font.render("Sin arma", True, (255,255,255)), (10,90))

    def render_game_over(self):
        self.win.fill((60,10,10))
        txt = self.big_font.render("Game Over", True, (255,255,255))
        rect = txt.get_rect(center=(400, 300))
        self.win.blit(txt, rect)
        sub = self.font.render(f"Muertes totales: {self.state.defeated}", True, (255,255,255))
        self.win.blit(sub, (rect.centerx - sub.get_width()/2, rect.centery + 50))
