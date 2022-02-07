"""
Author: Sharome Burton
Date: 01/20/2022

"""

import numpy as np
import random
import matplotlib.pyplot as plt

from rich import print


class Map:
    def __init__(self, size=(25, 25)):
        self.unknown_val = -1

        self.full_map = np.full((size[0], size[1]), self.unknown_val, dtype=int)
        self.size = size
        self.viewport = ViewPort([size[0]//2, size[1]//2], map_size=(size[0], size[1]))

    def get_map(self):
        return self.map

    def move_cam(self, direction, mag):

        row_view = self.viewport.coords[0]
        col_view = self.viewport.coords[1]
        n_rows_view, n_cols_view = self.viewport.view.shape

        if direction == 'up':
            if row_view > 0:
                self.viewport.coords[0] = self.viewport.coords[0] - mag
                print(f"Camera moved: {direction}, \nnew coord {self.viewport.coords}!!!!!")
                return self.viewport.coords

            else:
                print(f"Camera move {direction} not possible!!!!!")

        if direction == 'down':
            if row_view + n_rows_view < self.viewport.size[0]:
                self.viewport.coords[0] = self.viewport.coords[0] + mag
                print(f"Camera moved: {direction}, \nnew coord {self.viewport.coords}!!!!!")
                return self.viewport.coords


        if direction == 'left':
            if col_view > 0:
                self.viewport.coords[1] = self.viewport.coords[1] - mag
                print(f"Camera moved: {direction}, \nnew coord {self.viewport.coords}!!!!!")
                return self.viewport.coords

        if direction == 'right':
            if col_view + n_cols_view < self.viewport.size[1]:
                self.viewport.coords[1] = self.viewport.coords[1] + mag
                print(f"Camera moved: {direction}, \nnew coord {self.viewport.coords}!!!!!")
                return self.viewport.coords

        return self.viewport.coords

    def show_map(self):
        # print(self.full_map)
        plt.clf()
        plt.matshow(self.full_map, fignum=2)
        # plt.plot(self.view)
        plt.colorbar()
        plt.show(block=False)
        plt.pause(0.2)
        # plt.close("all")

    def show_view(self):
        print(self.viewport.show_view())

    def update_map(self):
        coords = self.viewport.coords
        view = self.viewport.view

        view_row, view_col = view.shape
        map_row, map_col = coords

        for row in range(0, view_row):

            for col in range(0, view_col):
                self.full_map[map_row + row][map_col + col] = view[row][col]


class ViewPort:
    def __init__(self, coords, size=(3, 3), map_size=(32, 32)):
        self.view = np.zeros((size[1], size[0]), dtype=int)
        self.size = size
        self.coords = coords # middle of map

    def get_view(self):
        return self.view

    def show_view(self):
        # print(self.view)
        # plt.figure(1)
        plt.clf()
        plt.matshow(self.view, fignum=1)
        # plt.plot(self.view)
        plt.colorbar()
        plt.show(block=False)
        plt.pause(0.2)
        # plt.close("all")


    def rand_update(self, n_cells):
        """
        pass
        """

        print(self.view.shape)
        for cell in range(0, n_cells+1):
            x = random.randint(0, self.size[1]-1)
            y = random.randint(0, self.size[0]-1)

            self.view[x][y] = random.randint(0, 2)
