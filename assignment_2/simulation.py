"""Simulation File for Handling a Grid and Running a Simulation"""
import numpy as np
from cell import Cell
class Simulation:
    def __init__(self, step: float, alpha: float, beta: float, gamma: float, rho: float, rows: int, cols: int):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.rho = rho

        self.rows = rows
        self.cols = cols

        # 0: Hesitant, 1: Not Hesitant, 2: Unsure
        self.rate_map = {(0, 1): (2, alpha), (1, 0): (2, beta), (1, 2): (1 ,gamma), (0, 2): (0, rho)}

        grid_layout = np.random.choice(3, (rows, cols))
        self.grid = self.__map_cells(grid_layout)

    def __map_cells(self, grid):
        create_cell = lambda val: Cell(val)
        vmap_cells = np.vectorize(create_cell)
        # print(i, j)
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
        if i == 0 and j == self.cols:
            return [(i + 1, j), (i, j - 1)]
        if i == self.rows and j == 0:
            return [(i - 1, j), (i, j + 1)]
        if i == self.rows and j == self.cols:
            return [(i - 1, j), (i, j - 1)]
        if i == 0:
            return [(i, j - 1), (i, j + 1), (i + 1, j)]
        if i == self.rows:
            return [(i, j - 1), (i, j + 1), (i - 1, j)]
        if j == 0:
            return [(i - 1, j), (i + 1, j), (i, j + 1)]
        if j == self.cols:
            return [(i - 1, j), (i + 1, j), (i, j - 1)]

        return [(i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)]

    def __update_cell(self, i, j):
        coordinate_lst = self.get_coordinate_list(i, j)
        print(i, j, coordinate_lst)

        cell = self.grid[i, j]

        sum_array = np.zeros(3)
        cell_hs = cell.hesitancy_state
        for c in coordinate_lst:
            c_hs = self.grid[c[0], c[1]].hesitancy_state
            if c_hs == cell_hs:
                continue

            rate_key = (c_hs, cell_hs)
            if rate_key not in self.rate_map.keys():
                continue

            sum_state, val = self.rate_map[rate_key]

        max_index = sum_array.argmax()
        cell.update(max_index, sum_array[max_index])

    def step(self):
        vupdate_cell = np.vectorize(self.__update_cell)
        copy_grid = np.fromfunction(vupdate_cell, self.grid.shape)
        self.grid = copy_grid
        print(self.grid)



    def update_grid(self):
        pass

s = Simulation(10, 10, 10, 10, 10, 2, 2)

s.step()
