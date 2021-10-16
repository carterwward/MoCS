"""Cell Class for Vaccine Hesitancy Model"""
from enum import Enum


class HesitancyState(Enum):
    """Numerical representation of state."""
    HESITANT = 0
    NOT_HESITANT = 1
    UNSURE = 2


class OpenMindedness(Enum):
    """Ranges represented by tuple for open mindedness factor."""
    HESITANT = ()
    NOT_HESITANT = ()
    UNSURE = ()


class Cell:
    def __init__(self, hesitancy_state: HesitancyState, row: int, col: int):
        pass

    def update(self):
        pass
