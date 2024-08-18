from enum import Enum

import pygame
from src.components.field import GameField, CellState
from src.components.settings import GameSettings


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    def __init__(self, field: GameField, start_pos: tuple[int, int], settings: GameSettings, length: int = 3,):
        self.field = field
        self.settings = settings
        self.direction = Direction.UP
        self.body = [(start_pos[0], start_pos[1] + i) for i in range(length)]
        self.grow_flag = False
        self.load_sprites()

        for x, y in self.body:
            self.field.update_cell(x, y, CellState.SNAKE_BODY)
        self.field.update_cell(self.body[0][0], self.body[0][1], CellState.SNAKE_HEAD)

    def load_sprites(self):
        self.head_sprites = {
            Direction.UP: pygame.image.load('assets/snake/snake_head_up.png'),
            Direction.DOWN: pygame.image.load('assets/snake/snake_head_down.png'),
            Direction.LEFT: pygame.image.load('assets/snake/snake_head_left.png'),
            Direction.RIGHT: pygame.image.load('assets/snake/snake_head_right.png')
        }
        for direction, sprite in self.head_sprites.items():
            self.head_sprites[direction] = pygame.transform.scale(sprite, (self.settings.cell_size, self.settings.cell_size))

        self.body_sprite = pygame.image.load('assets/snake/snake_body.png')
        self.body_sprite = pygame.transform.scale(self.body_sprite, (self.settings.cell_size, self.settings.cell_size))

    def move(self):
        apple_exists, score = True, 0
        head_x, head_y = self.body[0]
        move_x, move_y = self.direction.value
        new_head = (head_x + move_x, head_y + move_y)

        if (((new_head[0] < 0 or new_head[0] >= self.field.width // self.settings.cell_size or
            new_head[1] < 0 or new_head[1] >= self.field.height // self.settings.cell_size) or
                self.field.cells[new_head[1]][new_head[0]].state == CellState.SNAKE_BODY) or
                self.field.cells[new_head[1]][new_head[0]].state == CellState.WALL):
            return 1, apple_exists, score

        cell_state = self.field.cells[new_head[1]][new_head[0]].state
        cell = self.field.cells[new_head[1]][new_head[0]]
        self.grow(cell_state)

        if not self.grow_flag:
            tail_x, tail_y = self.body.pop()
            self.field.update_cell(tail_x, tail_y, CellState.EMPTY)
        else:
            apple_exists = False
            self.grow_flag = False
            score = cell.score

        self.body.insert(0, new_head)
        self.field.update_cell(new_head[0], new_head[1], CellState.SNAKE_HEAD)
        self.field.update_cell(self.body[1][0], self.body[1][1], CellState.SNAKE_BODY)
        return 0, apple_exists, score

    def grow(self, cell_state: CellState):
        if cell_state == CellState.FRUIT:
            self.grow_flag = True

    def change_direction(self, direction: Direction):
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        if direction != opposite_directions[self.direction]:
            self.direction = direction

    def draw(self, screen, field_position):
        for i, (x, y) in enumerate(self.body):
            position = (field_position[0] + x * self.settings.cell_size, field_position[1] + y * self.settings.cell_size)
            if i == 0:
                screen.blit(self.head_sprites[self.direction], position)
            else:
                screen.blit(self.body_sprite, position)

