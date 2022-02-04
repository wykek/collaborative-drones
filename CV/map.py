"""
Author: Sharome Burton
Date: 01/20/2022

"""

import numpy as np
import random

from rich import print

class Map:
    def __init__(self, size = (160,90)):
        self.full_map = np.zeros((size[1],size[0]), dtype=int)
        self.size = size
        self.viewport = ViewPort()

    def show_map(self):
        print(self.full_map)

    def show_view(self):
        print(self.viewport.show_view())

class ViewPort:
    def __init__(self, size = (16,9)):
        self.view = np.zeros((size[1],size[0]), dtype=int)
        self.size = size
        self.coords = (80,45)

    def show_view(self):
        print(self.view)


    def rand_update(self, n_cells):
        """
        pass
        """

        print(self.view.shape)
        for cell in range(0, n_cells+1):
            x = random.randint(0,self.size[1]-1)
            y = random.randint(0,self.size[0]-1)

            self.view[x][y] = random.randint(0,2)



