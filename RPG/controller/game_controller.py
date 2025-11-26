import pygame
import traceback
from model.game_state import GameState
from view.renderer import Renderer

class GameController:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.state = GameState()
        self.renderer = Renderer(window, self.state)

    def handle_input(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_e:
                    p = self.state.player
                    if p.current_weapon:
                        p.equipped = not p.equipped
                if ev.key == pygame.K_SPACE:
                    p = self.state.player
                    if p.equipped and p.current_weapon and p.current_weapon.get("ranged", False):
                        self.state.spawn_arrow()
                    else:
                        p.start_attack()

        # Movimiento con teclas presionadas
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.state.player.move(dx, dy)

        return True

    def update(self):
        self.state.update()

    def run(self):
        running = True
        try:
            while running:
                dt = self.clock.tick(self.state.FPS)
                running = self.handle_input()
                self.update()
                self.renderer.render()

                # Check lose condition and show game-over screen then break
                if self.state.player.health <= 0:
                    self.state.player.health = 0
                    self.renderer.render_game_over()
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    break

        except Exception:
            # Print traceback so puedas verlo si la ventana se cierra
            traceback.print_exc()
            # mantén la ventana abierta un segundo para que veas el error
            pygame.time.wait(1500)
