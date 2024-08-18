import pygame


class End:
    def __init__(self, screen, score, font, small_font, colors):
        self.screen = screen
        self.score = score
        self.font = font
        self.small_font = small_font
        self.colors = colors

    def draw(self):
        self.screen.fill(self.colors.frame_color)

        lose_text = self.font.render('You Lose!', True, (255, 255, 1))
        lose_rect = lose_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 3))
        self.screen.blit(lose_text, lose_rect)

        score_text = self.small_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(score_text, score_rect)

        info_text = self.small_font.render('Press space to play again', True, (255, 255, 255))
        info_rect = lose_text.get_rect(center=(self.screen.get_width() // 2 - 65, self.screen.get_height() // 2 + 50))
        self.screen.blit(info_text, info_rect)

        pygame.display.flip()

    @staticmethod
    def wait_for_quit():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return 0
