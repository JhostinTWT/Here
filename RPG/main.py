import pygame
from controller.game_controller import GameController

pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mini RPG - MVC (corregido)")

game = GameController(window)
game.run()

pygame.quit()
