import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Union

from src.components.settings import GameSettings


class CellState(Enum):
    EMPTY = 0
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    FRUIT = 3


class Cell:
    def __init__(self, state: CellState):
        self.state = state


class Fruit(Cell):
    def __init__(self, sprite, score, state):
        self.sprite = sprite
        self.score = score
        super().__init__(state)


@dataclass
class GameField:
    width: int
    height: int
    settings: GameSettings
    cells: list[list[Union[Cell, Fruit]]] = field(default_factory=list)

    def __post_init__(self):
        self.cells = [[Cell(CellState.EMPTY) for _ in range(self.width // self.settings.cell_size + 1)] for _ in range(self.height // self.settings.cell_size + 1)]

    def update_cell(self, x: int, y: int, state: CellState, sprite=None, score=None):
        if state == CellState.FRUIT:
            self.cells[y][x] = Fruit(sprite, score, state)
        else:
            self.cells[y][x] = Cell(state)

    def get_random_empty_cell(self):
        empty_cells = [(x, y) for y in range(len(self.cells))
                       for x in range(len(self.cells[0]))
                       if self.cells[y][x].state == CellState.EMPTY]
        if empty_cells:
            return random.choice(empty_cells)
        return None
