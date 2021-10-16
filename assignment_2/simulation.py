"""Simulation File for Handling a Grid and Running a Simulation"""
import numpy as np
from cell import Cell

class Simulation:
    def __init__(self, alpha: float, beta: float, gamma: float, rho: float, rows: int, cols: int):
        # np.random.seed(1)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.rho = rho
        self.rows = rows
        self.cols = cols

        self.rows = rows
        self.cols = cols

        # 0: Hesitant, 1: Not Hesitant, 2: Unsure
        self.rate_map = {(0, 1): (2, alpha), (1, 0): (2, beta), (1, 2): (1 ,gamma), (0, 2): (0, rho)}

        grid_layout = np.random.choice(3, (rows, cols))
        self.grid = self.__map_cells(grid_layout)
        self.neighborhood_map = self.__neighborhood_map()

    def __map_cells(self, grid):
        create_cell = lambda val: Cell(val)
        vmap_cells = np.vectorize(create_cell)
        # print(i, j)
        return vmap_cells(grid)

    def __neighborhood_map(self):
        """Create neighborhood map of all neighbors up down left or right."""
        neighborhood = {}

        def _get_coordinate_list(i, j):
            """Gets list of lower, higher, left, and right cell."""
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
                neighborhood[(i, j)] = _get_coordinate_list(i, j)

        return neighborhood


    def __update_cell(self, i, j):
        i = int(i)
        j = int(j)
        coordinate_lst = self.neighborhood_map[(i, j)]
        cell = self.grid[i, j]
        if i == 1 and j == 1:
            print("THE CELL WE CARE ABOUT")

        sum_array = np.zeros(3)
        cell_hs = cell.hesitancy_state
        if i == 1 and j == 1:
            print("HES STATE", cell_hs)
        if i == 1 and j == 1:
            print("SURROUNDING CELLS")
        for c in coordinate_lst:
            c_hs = self.grid[c[0], c[1]].hesitancy_state
            if i == 1 and j == 1:
                print("coord", c, "hesitancy status",c_hs)
            if c_hs == cell_hs:
                continue

            rate_key = (c_hs, cell_hs)
            if rate_key not in self.rate_map.keys():
                continue

            sum_state, val = self.rate_map[rate_key]
            sum_array[sum_state] += val
        if i == 1 and j == 1:
            print("SUM ARRAY:", sum_array)
        max_index = sum_array.argmax()
        cell.update(max_index, sum_array[max_index])
        if i == 1 and j == 1:
            print("NEW STATUS:", cell.hesitancy_state)

        return cell

    def step(self):
        vupdate_cell = np.vectorize(self.__update_cell)
        copy_grid = np.fromfunction(vupdate_cell, self.grid.shape)
        self.grid = copy_grid

s = Simulation(0.1, 0.1, 0.1, 0.1, 3, 3)
for i in range(1):
    s.step()
    print("\n")
