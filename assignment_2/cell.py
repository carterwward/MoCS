"""Cell Class for Vaccine Hesitancy Model"""
from typing import Union
import numpy as np


class Cell:
    def __init__(self, hesitancy_state: int):
        """Initialize instance of Cell class, representing a person with a given HesitancyState.

        Args:
            hesitancy_state (int): initial hesitancy state of person
            row (int): row in grid
            column (int): column in grid
        """
        self.hesitancy_state = hesitancy_state
        self.open_mindedness = None

        self.get_open_mindedness_value()  # dependent on self.open_mindedness

    def get_open_mindedness_value(self):
        """get open_mindedness value from the current self.hesitancy_state."""
        if self.hesitancy_state == 0:
            self.open_mindedness = np.random.uniform(0.2, 0.5)

        elif self.hesitancy_state == 1:
            self.open_mindedness = np.random.uniform(0.2, 0.5)

        elif self.hesitancy_state == 2:
            self.open_mindedness = np.random.uniform(0, 0.2)

    def open_mindedness_noise(self):
        """Random noise for open_mindedness state."""
        self.open_mindedness += np.random.uniform(-0.2, 0.2)

    def update(self, max_state_in_neighborhood: int, new_state_influence: float):
        """Update the cell based on value calculated from it's neighbords in simulation.py"""
        if new_state_influence > self.open_mindedness:
            self.hesitancy_state = max_state_in_neighborhood
            self.get_open_mindedness_value()

        self.open_mindedness_noise()

    @property
    def color(self):
        """Get the color of a cell for visualization.

        Returns:
            tuple: (r, g, b) tuple determined by the self.hesitancy_state
        """
        if self.hesitancy_state == 0:
            return (255, 0, 0)  # red

        elif self.hesitancy_state == 1:
            return (0, 128, 0)  # green

        elif self.hesitancy_state == 2:
            return (255, 255, 255)  # white
