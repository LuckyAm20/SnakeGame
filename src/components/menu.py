import pygame

from src.utils.utils import load_highscore


class Menu:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.button_rect = pygame.Rect(230, 350, 130, 70)
        self.highscore = load_highscore()

    def draw(self):
        self.screen.fill(self.colors.frame_color)
        title_text = self.font.render('Snake Game', True, (255, 255, 255))
        play_text = self.font.render('Play', True, (255, 255, 255))
        highscore_text = self.small_font.render(f'Highscore: {self.highscore}', True, (255, 255, 255))

        self.screen.blit(title_text, (140, 100))
        pygame.draw.rect(self.screen, (255, 0, 0), self.button_rect)
        self.screen.blit(play_text, (self.button_rect.x + 10, self.button_rect.y + 10))
        self.screen.blit(highscore_text, (220, 500))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return 'play'
        return None
