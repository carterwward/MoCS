"""Cell Class for Vaccine Hesitancy Model"""
from enum import Enum
import numpy as np


class HesitancyState(Enum):
    """Numerical representation of state."""
    HESITANT = 0
    NOT_HESITANT = 1
    UNSURE = 2


class Cell:
    def __init__(self, hesitancy_state: HesitancyState, row: int, column: int):
        """Initialize instance of Cell class, representing a person with a given HesitancyState.

        Args:
            hesitancy_state (HesitancyState): initial HesitancyState of person
            row (int): row in grid
            column (int): column in grid
        """
        self.hesitancy_state = hesitancy_state
        self.row = row
        self.column = column
        self.open_mindedness = None

        self.get_open_mindedness_value()  # dependent on self.open_mindedness

    def get_open_mindedness_value(self):
        """get open_mindedness value from the current self.hesitancy_state."""
        if self.hesitancy_state == HesitancyState.HESITANT:
            self.open_mindedness = np.random.uniform(0.2, 0.5)

        elif self.hesitancy_state == HesitancyState.NOT_HESITANT:
            self.open_mindedness = np.random.uniform(0.2, 0.5)

        elif self.hesitancy_state == HesitancyState.UNSURE:
            self.open_mindedness = np.random.uniform(0, 0.2)

    def open_mindedness_noise(self):
        """Random noise for open_mindedness state."""
        self.open_mindedness += np.random.uniform(-0.2, 0.2)

    def update(self, max_state_in_neighborhood: HesitancyState, new_state_influence: float):
        """Update the cell based on value calculated from it's neighbords in simulation.py"""
        if new_state_influence > self.open_mindedness:
            self.hesitancy_state = max_state_in_neighborhood
            self.get_open_mindedness_value()

        self.open_mindedness_noise()

    @property
    def color(self):
        if self.hesitancy_state == HesitancyState.HESITANT:
            return (255, 0, 0)  # red

        elif self.hesitancy_state == HesitancyState.NOT_HESITANT:
            return (0, 128, 0)  # green

        elif self.hesitancy_state == HesitancyState.UNSURE:
            return (255, 255, 255)  # white
