"""Simulation File for Handling a Grid and Running a Simulation"""
import numpy as np
from src.cell import Cell
import matplotlib.pyplot as plt
from time import time
import os

class Simulation:
    def __init__(self, alpha: float, beta: float, gamma: float, rho: float, rows: int, cols: int, steps: int):
        # np.random.seed(1)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.rho = rho
        self.rows = rows
        self.cols = cols

        self.rows = rows
        self.cols = cols
        self.iteration = 0
        self.steps = steps

        self.data_matrix = np.zeros((steps, 3), int)

        # 0: Hesitant, 1: Not Hesitant, 2: Unsure
        self.rate_map = {(0, 1): (2, alpha), (1, 0): (2, beta), (1, 2): (1 ,gamma), (0, 2): (0, rho)}

        grid_layout = np.random.choice(3, (rows, cols))
        self.grid = self.__map_cells(grid_layout)
        self.__update_counts()

        self.neighborhood_map = self.__neighborhood_map()


    def __update_counts(self):
        get_hesitancy = lambda c: c.hesitancy_state
        vget_hesitancy = np.vectorize(get_hesitancy)

        num_grid = vget_hesitancy(self.grid)
        unique, counts = np.unique(num_grid, return_counts=True)
        val_counts = dict(zip(unique, counts))

        for i in range(3):
            if i not in val_counts.keys():
                val_counts[i] = 0

        self.data_matrix[self.iteration, :] = np.array([val_counts[0], val_counts[1], val_counts[2]])
        self.iteration += 1


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
                return [(i, j+1), (i+1, j), (i+1,j+1)]
            elif i == 0 and j == self.cols - 1:
                return [(i, j-1), (i+1, j), (i+1, j-1)]
            elif i == self.rows - 1 and j == 0:
                return [(i-1, j), (i, j+1), (i-1, j+1)]
            elif i == self.rows - 1 and j == self.cols - 1:
                return [(i, j-1), (i-1, j), (i-1,j-1)]
            elif i == 0:
                return [(i+1, j), (i, j-1), (i, j+1), (i+1, j+1), (i+1, j-1)]
            elif i == self.rows - 1:
                return [(i-1, j), (i, j-1), (i, j+1), (i-1, j+1), (i-1, j-1)]
            elif j == 0:
                return [(i, j+1), (i-1, j), (i+1, j), (i-1, j+1), (i+1, j+1)]
            elif j == self.cols - 1:
                return [(i, j-1), (i-1, j), (i+1, j), (i-1, j-1), (i+1, j-1)]
            else:
                return [(i, j-1), (i, j+1), (i+1, j), (i-1, j), (i+1, j+1), (i+1, j-1), (i-1, j-1), (i-1, j+1)]

        for i in range(self.rows):
            for j in range(self.cols):
                neighborhood[(i, j)] = _get_coordinate_list(i, j)

        return neighborhood


    def __update_cell(self, i, j):
        i = int(i)
        j = int(j)
        coordinate_lst = self.neighborhood_map[(i, j)]
        cell = self.grid[i, j]
        # important_row = 1
        # important_col = 1
        # if i == important_row and j == important_col:
        #     print("THE CELL WE CARE ABOUT")

        sum_array = np.zeros(3)
        cell_hs = cell.hesitancy_state
        # if i == important_row and j == important_col:
        #     print("HES STATE", cell_hs)
        # if i == important_row and j == important_col:
        #     print("SURROUNDING CELLS")
        for c in coordinate_lst:
            c_hs = self.grid[c[0], c[1]].hesitancy_state
            # if i == important_row and j == important_col:
            #     print("coord", c, "hesitancy status",c_hs)
            if c_hs == cell_hs:
                continue

            rate_key = (c_hs, cell_hs)
            if rate_key not in self.rate_map.keys():
                continue

            sum_state, val = self.rate_map[rate_key]
            sum_array[sum_state] += val
        # if i == important_row and j == important_col:
        #     print("SUM ARRAY:", sum_array)
        max_index = sum_array.argmax()
        cell.update(max_index, sum_array[max_index])
        # if i == important_row and j == important_col:
        #     print("NEW STATUS:", cell.hesitancy_state)

        return cell

    def step(self):
        vupdate_cell = np.vectorize(self.__update_cell)
        copy_grid = np.fromfunction(vupdate_cell, self.grid.shape)
        self.grid = copy_grid
        self.__update_counts()


    # TODO: This can be updated for better graphics
    def graph_counts(self):
        plt.plot(self.data_matrix[:, 0], label="Hesitant", color="red")
        plt.plot(self.data_matrix[:, 1], label="Non-hesitant", color="green")
        plt.plot(self.data_matrix[:, 2], label="Unsure", color="blue")
        plt.legend(loc='upper right')
        plt.xlabel("Time Step")
        plt.ylabel("Population")
        plt.title("Category Population Over Time")
        plt.savefig(os.path.join("assignment_2","graphs", str(time())+".jpg"))
