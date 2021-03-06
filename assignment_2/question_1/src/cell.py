"""Cell Class for Vaccine Hesitancy Model"""
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

        self.__get_open_mindedness_value()  # dependent on self.open_mindedness

    def __get_open_mindedness_value(self):
        # TODO: Idea to make O.P. a function of similar mindedness around them (specifically for N and H)
        """get open_mindedness value from the current self.hesitancy_state."""
        # Hesitant
        if self.hesitancy_state == 0:
            # self.open_mindedness = 0.4
            self.open_mindedness = np.random.uniform(0.0, 0.15)
        # Non-hesitant
        elif self.hesitancy_state == 1:
            # self.open_mindedness = 0.4
            self.open_mindedness = np.random.uniform(0.0, 0.15)
        # Unsure
        elif self.hesitancy_state == 2:
            # self.open_mindedness = 0.4
            self.open_mindedness = np.random.uniform(0.0, 0.15)

    # def __open_mindedness_noise(self):
    #     """Random noise for open_mindedness state."""
    #     self.open_mindedness += np.random.uniform(-0.2, 0.2)

    def update(self, max_state_in_neighborhood: int, new_state_influence: float):
        """Update the cell based on value calculated from it's neighbords in simulation.py"""
        if new_state_influence >= self.open_mindedness:
            self.hesitancy_state = max_state_in_neighborhood
            self.__get_open_mindedness_value()

        # self.__open_mindedness_noise()

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
            return (0, 0, 255)  # blue
