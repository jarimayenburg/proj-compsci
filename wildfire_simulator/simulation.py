#
# Contains the simulation class, the outermost class of the whole simulation.
#

from ca import CA


class Simulation:
    def __init__(self, grid_filename):
        self.ca = CA.from_file(grid_filename)

    def run(self):
        pass
