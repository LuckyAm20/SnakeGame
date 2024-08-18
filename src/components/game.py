import json
import random

import pygame

from src.components.end import End
from src.components.field import GameField, CellState
from src.components.menu import Menu
from src.components.settings import GameSettings, Colors
from src.components.snake import Snake, Direction
from src.utils.utils import load_highscore


class Game:
    def __init__(self, settings: GameSettings, colors: Colors):
        self.settings = settings
        self.colors = colors
        self.score = 0
        self.game_over = False
        self.size = self.settings.window_size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.settings.name)
        self.menu = Menu(self.screen, colors)
        self.highscore = load_highscore()
        self.small_font = pygame.font.Font(None, 36)
        self.game_running = False

        self.field_size = self.settings.field_size
        self.field_position = [(self.size[0] - self.field_size[0]) // 2,
                               (self.size[1] - self.field_size[1]) // 2 + 50]

        border_sprite_up = pygame.image.load('assets/borders/border_up.png')
        self.border_sprite_up = pygame.transform.scale(border_sprite_up, (self.settings.border_width, self.settings.border_width))
        border_sprite_down = pygame.image.load('assets/borders/border_down.png')
        self.border_sprite_down = pygame.transform.scale(border_sprite_down, (self.settings.border_width, self.settings.border_width))
        border_sprite_right = pygame.image.load('assets/borders/border_right.png')
        self.border_sprite_right = pygame.transform.scale(border_sprite_right, (self.settings.border_width, self.settings.border_width))
        border_sprite_left = pygame.image.load('assets/borders/border_left.png')
        self.border_sprite_left = pygame.transform.scale(border_sprite_left, (self.settings.border_width, self.settings.border_width))
        border_sprite_corner = pygame.image.load('assets/borders/border_corner.png')
        self.border_sprite_corner = pygame.transform.scale(border_sprite_corner, (self.settings.border_width, self.settings.border_width))

        snake_head_up = pygame.image.load('assets/snake/snake_head_up.png')
        self.snake_head_up = pygame.transform.scale(snake_head_up, (self.settings.cell_size, self.settings.cell_size))

        snake_body = pygame.image.load('assets/snake/snake_body.png')
        self.snake_body = pygame.transform.scale(snake_body, (self.settings.cell_size, self.settings.cell_size))

        apple = pygame.image.load('assets/food/apple.png')
        apple = pygame.transform.scale(apple, (self.settings.cell_size, self.settings.cell_size))
        cherry = pygame.image.load('assets/food/cherry.png')
        cherry = pygame.transform.scale(cherry, (self.settings.cell_size, self.settings.cell_size))
        grape = pygame.image.load('assets/food/grape.png')
        grape = pygame.transform.scale(grape, (self.settings.cell_size, self.settings.cell_size))
        pear = pygame.image.load('assets/food/pear.png')
        pear = pygame.transform.scale(pear, (self.settings.cell_size, self.settings.cell_size))
        strawberry = pygame.image.load('assets/food/strawberry.png')
        strawberry = pygame.transform.scale(strawberry, (self.settings.cell_size, self.settings.cell_size))
        self.fruits = [(apple, 10), (cherry, 50), (grape, 100), (pear, 150), (strawberry, 200)]


        pygame.font.init()
        self.font = pygame.font.SysFont(None, 50)

    def draw_borders(self):
        self.screen.blit(self.border_sprite_corner, (self.field_position[0] - self.settings.border_width, self.field_position[1] - self.settings.border_width))
        self.screen.blit(self.border_sprite_corner,
                         (self.field_position[0] + self.field_size[0], self.field_position[1] - self.settings.border_width))
        for x in range(self.field_position[0], self.field_position[0] + self.field_size[0], self.settings.border_width):
            self.screen.blit(self.border_sprite_up, (x, self.field_position[1] - self.settings.border_width))

        for x in range(self.field_position[0], self.field_position[0] + self.field_size[0], self.settings.border_width):
            self.screen.blit(self.border_sprite_down, (x, self.field_position[1] + self.field_size[1]))

        self.screen.blit(self.border_sprite_corner,
                         (self.field_position[0] + self.field_size[0],
                          self.field_position[1] - self.settings.border_width))

        self.screen.blit(self.border_sprite_corner,
                         (self.field_position[0] - self.settings.border_width,
                          self.field_position[1] + self.field_size[1]))
        self.screen.blit(self.border_sprite_corner, (self.field_position[0] + self.field_size[0], self.field_position[1] + self.field_size[1]))
        for y in range(self.field_position[1], self.field_position[1] + self.field_size[1], self.settings.border_width):
            self.screen.blit(self.border_sprite_left, (self.field_position[0] - self.settings.border_width, y))

        for y in range(self.field_position[1], self.field_position[1] + self.field_size[1], self.settings.border_width):
            self.screen.blit(self.border_sprite_right, (self.field_position[0] + self.field_size[0], y))

    def draw_field(self):
        for y in range(self.game_field.height // self.settings.cell_size):
            for x in range(self.game_field.width // self.settings.cell_size):
                cell = self.game_field.cells[y][x]
                position = (self.field_position[0] + x * self.settings.cell_size,
                            self.field_position[1] + y * self.settings.cell_size)

                if cell.state == CellState.SNAKE_HEAD:
                    self.screen.blit(self.snake_head_up, position)
                elif cell.state == CellState.SNAKE_BODY:
                    self.screen.blit(self.snake_body, position)
                elif cell.state == CellState.FRUIT:
                    self.screen.blit(cell.sprite, position)
                elif cell.state == CellState.WALL:
                    self.screen.blit(self.border_sprite_corner, position)
                else:
                    pygame.draw.rect(self.screen, self.colors.field_color,
                                     (position[0], position[1], self.settings.cell_size, self.settings.cell_size))

    def place_random_apple(self):
        if not self.apple_exists:
            position = self.game_field.get_random_empty_cell()
            if position:
                sprite, score = random.choice(self.fruits)
                self.game_field.update_cell(position[0], position[1], CellState.FRUIT, sprite, score)
                self.apple_exists = True

    def place_random_wall(self):
        position = self.game_field.get_random_empty_cell()
        if position:
            self.game_field.update_cell(position[0], position[1], CellState.WALL)

    @staticmethod
    def save_highscore(score):
        try:
            with open('highscore.json', 'w') as file:
                json.dump({'highscore': score}, file)
        except IOError:
            print("Error saving highscore.")

    def draw_score(self):
        score_label = self.font.render("Score:", True, self.colors.text_color)
        self.screen.blit(score_label, (self.size[0] - 250, self.field_position[1] - 80))

        score_value = self.font.render(str(self.score), True, self.colors.text_color)
        score_value_position = (self.size[0] - 250 + score_label.get_width() + 10, self.field_position[1] - 80)
        self.screen.blit(score_value, score_value_position)

    def start_game(self):
        self.apple_exists = False
        self.apple_timer = 0
        self.apple_interval = random.randint(3000, 8000)

        self.wall_timer = 0
        self.wall_interval = random.randint(8000, 12000)

        self.game_field = GameField(self.field_size[0], self.field_size[1], self.settings)
        self.game_field.update_cell(5, 5, CellState.SNAKE_HEAD)
        self.game_field.update_cell(5, 6, CellState.SNAKE_BODY)
        self.snake = Snake(self.game_field, (5, 6), self.settings)
        self.play_game()

    def play_game(self):
        clock = pygame.time.Clock()
        while True:
            current_time = pygame.time.get_ticks()

            if not self.apple_exists and current_time - self.apple_timer > self.apple_interval:
                self.place_random_apple()
                self.apple_timer = current_time
                self.apple_interval = random.randint(2000, 5000)

            if current_time - self.wall_timer > self.wall_interval:
                self.place_random_wall()
                self.wall_timer = current_time
                self.wall_interval = random.randint(8000, 12000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)

            game_over, apple_exists, score = self.snake.move()
            if game_over:
                self.end_game()
                return
            if not apple_exists:
                self.apple_exists = False
                self.settings.fps += 1
                self.score += score

            self.screen.fill(self.colors.frame_color)

            self.draw_borders()
            pygame.draw.rect(self.screen, self.colors.field_color,
                             (self.field_position[0], self.field_position[1],
                              self.field_size[0], self.field_size[1]))
            self.draw_field()
            self.draw_score()
            self.snake.draw(self.screen, self.field_position)
            pygame.display.flip()
            clock.tick(self.settings.fps)

    def end_game(self):
        self.game_running = False

        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore(self.highscore)

        end = End(self.screen, self.score, self.font, self.small_font, self.colors)
        end.draw()
        self.game_running = False
        self.score = 0
        self.settings.fps = 5
        if end.wait_for_quit():
            self.game_over = True

    def run(self):
        while True:
            if self.game_over:
                pygame.quit()
                return
            if not self.game_running:
                self.show_menu()
            else:
                self.start_game()

    def show_menu(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    return

                result = self.menu.handle_event(event)
                if result == 'play':
                    self.game_running = True
                    return

            self.menu.draw()
            pygame.display.flip()
            clock.tick(30)
