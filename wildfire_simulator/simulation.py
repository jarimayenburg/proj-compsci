"""Contains the simulation class, the outermost class of the simulation."""

from ca import CA, NNEvolutionRule
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Simulation:
    """Class simulating a wildfire."""

    def __init__(self, grid_filename, interval=300, seed=1):
        """
        Construct the simulation.

        Params:
        - grid_filename: Filename of the initial grid
        - interval: Amount of miliseconds between frames of the animation
        """

        # Evolution rule that evolves a cell based on its neighbors.
        evolution_rule = NNEvolutionRule()

        self.ca = CA.from_file(grid_filename, evolution_rule, seed)
        self.interval = interval

    def run(self):
        """Run the simulation."""
        # Disable imshow toolbar
        mpl.rcParams['toolbar'] = 'None'

        figure = plt.figure()
        frame = plt.imshow(self.ca.grid_as_pixels())

        # Animation function. Evolves the CA to the next step and draws it.
        def animate(i):
            self.ca.step()
            frame.set_data(self.ca.grid_as_pixels())

            return frame

        animation = FuncAnimation(figure, animate, interval=self.interval)
        plt.show()

    def burned_cells(self):
        """How many cells have burned down"""
        burned = 0

        for row in self.ca.grid:
            for cell in row:
                if cell.state == 2:
                    burned += 1

        return burned

    def scar_size(self):
        """monitor the size of the burn scar over time"""

        burned = self.burned_cells()
        prev_burned = -1
        scar = np.array([burned])

        # while there are still cells burning
        while not prev_burned == burned:
            # step
            self.ca.step()

            # increment the data we are interested in
            prev_burned = burned
            burned = self.burned_cells()

            # remember the results
            scar = np.append(scar, burned)

        # and we are done
        return scar

    def scar_size_graph(self):
        """generate a graph of the size of the burn scar over time"""
        data = self.scar_size()

        plt.plot(data)
        plt.show()

