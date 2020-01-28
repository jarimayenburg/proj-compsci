"""Contains the simulation class, the outermost class of the simulation."""

from ca import CA, NNEvolutionRule
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Simulation:
    """Class simulating a wildfire."""

    def __init__(self, grid_filename, interval=100):
        """
        Construct the simulation.

        Params:
        - grid_filename: Filename of the initial grid
        - interval: Amount of miliseconds between frames of the animation
        """
        self.ca = CA.from_gridfile(grid_filename)
        self.interval = interval

    def run(self):
        """Run the simulation."""
        # Disable imshow toolbar
        mpl.rcParams['toolbar'] = 'None'

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        h, w = self.ca.grid.shape
        xs, ys = range(w), range(h)
        X, Y = np.meshgrid(xs, ys)
        Z = self.ca.get_altitudes()

        colors = self.ca.grid_as_pixels()
        plot = ax.plot_surface(X, Y, Z, facecolors=colors, rcount=h, ccount=w)

        # Animation function. Evolves the CA to the next step and draws it.
        def animate(i, plot):
            self.ca.step()
            colors = self.ca.grid_as_pixels()

            ax.clear()
            plot = ax.plot_surface(
                X, Y, Z, facecolors=colors,
                rcount=h, ccount=w
            )
            return plot

        animation = FuncAnimation(
            fig, animate, interval=self.interval, fargs=(plot,)
        )
        plt.show()

    def burned_cells(self):
        """How many cells have burned down."""
        burned = 0

        for row in self.ca.grid:
            for cell in row:
                if cell.state == 2:
                    burned += 1

        return burned

    def scar_size(self):
        """Monitor the size of the burn scar over time."""

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
        """Generate a graph of the size of the burn scar over time."""
        data = self.scar_size()

        plt.plot(data)
        plt.title("Size of the burn scar over time")
        plt.ylabel("Burned cells")
        plt.xlabel("Time step")
        plt.show()
