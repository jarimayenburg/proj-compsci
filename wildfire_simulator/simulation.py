"""Contains the simulation class, the outermost class of the simulation."""

from ca import CA
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt


class Simulation:
    """Class simulating a wildfire."""

    def __init__(self, grid_filename):
        """Construct the simulation."""
        self.ca = CA.from_file(grid_filename)

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

        animation = FuncAnimation(figure, animate, interval=1)
        plt.show()
