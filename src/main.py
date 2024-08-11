from src.components.game import Game
import pygame
from src.components.settings import GameSettings, Colors

if __name__ == '__main__':
    pygame.init()
    game = Game(GameSettings(), Colors())
    game.run()

