from dataclasses import dataclass, field
from enum import Enum
from src.components.settings import GameSettings


class CellState(Enum):
    EMPTY = 0
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    APPLE = 3


@dataclass
class GameField:
    width: int
    height: int
    settings: GameSettings
    cells: list[list[CellState]] = field(default_factory=list)

    def __post_init__(self):
        self.cells = [[CellState.EMPTY for _ in range(self.width // self.settings.cell_size + 1)] for _ in range(self.height // self.settings.cell_size + 1)]

    def update_cell(self, x: int, y: int, state: CellState):
        self.cells[y][x] = state