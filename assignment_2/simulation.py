"""Simulation File for Handling a Grid and Running a Simulation"""
import numpy as np
from cell import Cell
class Simulation:
    def __init__(self, step: float, alpha: float, beta: float, gamma: float, rho: float, rows: int, cols: int):
        self.alpha = alpha
        self.beta = beta
        self. gamma = gamma
        self.rho = rho

        grid_layout = np.random.choice(3, (rows, cols))
        self.grid = self.__map_cells(grid_layout)

    def __map_cells(self, grid):
        create_cell = lambda val: Cell(val)
        vmap_cells = np.vectorize(create_cell)
        return vmap_cells(grid)

    def step(self):
        pass

    def update_grid(self):
        pass

s = Simulation(10, 10, 10, 10, 10, 5, 5)
