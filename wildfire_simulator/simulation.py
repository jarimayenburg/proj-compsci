"""Contains the simulation class, the outermost class of the whole simulation."""

from ca import CA


class Simulation:
    """Class simulating a wildfire."""

    def __init__(self, grid_filename):
        """Construct the simulation."""
        self.ca = CA.from_file(grid_filename)

    def run(self):
        """Run the simulation."""
        pass
