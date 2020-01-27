"""Contains the simulation class, the outermost class of the simulation."""

from ca import CA, NNEvolutionRule
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt


class Simulation:
    """Class simulating a wildfire."""

    def __init__(self, grid_filename, interval=300):
        """
        Construct the simulation.

        Params:
        - grid_filename: Filename of the initial grid
        - interval: Amount of miliseconds between frames of the animation
        """

        # Evolution rule that evolves a cell based on its neighbors.
        evolution_rule = NNEvolutionRule()

        self.ca = CA.from_file(grid_filename, evolution_rule)
        self.interval = interval

    def run(self):
        """Run the simulation."""
        # Disable imshow toolbar
        mpl.rcParams['toolbar'] = 'None'

        figure = plt.figure()
        frame = plt.imshow(self.ca.grid_as_ints(), cmap=CA.STATE_COLORMAP)

        # Animation function. Evolves the CA to the next step and draws it.
        def animate(i):
            self.ca.step()
            frame.set_data(self.ca.grid_as_ints())

            return frame

        animation = FuncAnimation(figure, animate, interval=self.interval)
        plt.show()
