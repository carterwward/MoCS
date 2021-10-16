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
        print(i, j)
        return vmap_cells(grid)


    def get_coordinate_list(self, i, j):
    """gets list of lower, higher, left, and right cell
    Args:
        i (int): origin row index
        j (int): origin col index
    Returns:
        list: list of tuples of coordinates for grid
    """
        if i == 0 and j == 0:
            return [(i + 1, j), (i, j + 1)]
        if i == 0 and j == self.num_cols:
            return [(i + 1, j), (i, j - 1)]
        if i == self.num_rows and j == 0:
            return [(i - 1, j), (i, j + 1)]
        if i == self.num_rows and j == self.num_cols:
            return [(i - 1, j), (i, j - 1)]
        if i == 0:
            return [(i, j - 1), (i, j + 1), (i + 1, j)]
        if i == self.num_rows:
            return [(i, j - 1), (i, j + 1), (i - 1, j)]
        if j == 0:
            return [(i - 1, j), (i + 1, j), (i, j + 1)]
        if j == self.num_cols:
            return [(i - 1, j), (i + 1, j), (i, j - 1)]

        return [(i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)]

    def __update_cell(self, i, j):
        coords = self.get_coordinate_list(i, j)
        return 1 + i + j

    def step(self):
        vupdate_cell = np.vectorize(self.__update_cell)
        copy_grid = np.fromfunction(vupdate_cell, self.grid.shape)
        self.grid = copy_grid
        print(self.grid)



    def update_grid(self):
        pass

s = Simulation(10, 10, 10, 10, 10, 2, 2)

s.step()
