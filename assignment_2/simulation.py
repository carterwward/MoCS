"""Simulation File for Handling a Grid and Running a Simulation"""
import numpy as np
from cell import Cell
class Simulation:
    def __init__(self, step: float, alpha: float, beta: float, gamma: float, rho: float, rows: int, cols: int):
        self.alpha = alpha
        self.beta = beta
        self. gamma = gamma
        self.rho = rho
        self.rows = rows
        self.cols = cols

        grid_layout = np.random.choice(3, (rows, cols))
        self.grid = self.__map_cells(grid_layout)
        self.neighborhood_map = self.__neighborhood_map()
        for key in self.neighborhood_map.keys():
            print(key, self.neighborhood_map[key])

    def __map_cells(self, grid):
        create_cell = lambda val: Cell(val)
        vmap_cells = np.vectorize(create_cell)
        return vmap_cells(grid)

    def __neighborhood_map(self):
        neighborhood = {}

        def _get_coordinate_list(i, j):
            """gets list of lower, higher, left, and right cell."""
            if i == 0  and j == 0:
                return [(i, j+1), (i+1, j)]
            elif i == 0 and j == self.cols - 1:
                return [(i, j-1), (i+1, j)]
            elif i == self.rows - 1 and j == 0:
                return [(i-1, j), (i, j+1)]
            elif i == self.rows - 1 and j == self.cols - 1:
                return [(i, j-1), (1-1, j)]
            elif i == 0:
                return [(i+1, j), (i, j-1), (i, j+1)]
            elif i == self.rows - 1:
                return [(i-1, j), (i, j-1), (i, j+1)]
            elif j == 0:
                return [(i, j+1), (i-1, j), (i+1, j)]
            elif j == self.cols - 1:
                return [(i, j-1), (i-1, j), (i+1, j)]
            else:
                return [(i, j-1), (i, j+1), (i+1, j), (i-1, j)]

        for i in range(self.rows):
            for j in range(self.cols):
                # print(i, j)
                neighborhood[(i, j)] = _get_coordinate_list(i, j)

        return neighborhood


    def __update_cell(self, i, j):
        coords = self.get_coordinate_list(i, j)
        return 1 + i + j

    def step(self):
        vupdate_cell = np.vectorize(self.__update_cell)
        copy_grid = np.fromfunction(vupdate_cell, self.grid.shape)
        self.grid = copy_grid



    def update_grid(self):
        pass

s = Simulation(10, 10, 10, 10, 10, 3, 3)

